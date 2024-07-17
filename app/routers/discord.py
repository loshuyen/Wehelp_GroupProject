from fastapi import *
from fastapi.responses import JSONResponse
from typing import Annotated
import requests
import json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .weather import get_weather_by_county
from .warning import fetch_hotindex, fetch_uv
from config.basemodel import *


router = APIRouter()

@router.get("/api/send_discord_message",
            summary="依照Query傳入的縣市取得後端資料並向Discord Wehelp/bot 頻道發送模板訊息",
            responses={
                200: {'description': "資料傳送成功"},
                400: {'model': Error, 'description': '資料取得失敗，輸入不正確或其他原因'},
                422: {'model': Error,
                      'description': "輸入格式錯誤"
                      },
                500: {'model': Error, 'description': '伺服器內部錯誤'}
            })
async def discord_bot(request: Request, weather: Annotated[dict, Depends(lambda county_name='臺北市': get_weather_by_county(county_name))], hot: Annotated[dict, Depends(fetch_hotindex)], uv: Annotated[dict, Depends(fetch_uv)]):
    
    # get data from Depends
    api_array_list = []
    # county_name = weather.values()['county_name']
    for data in weather.values():
        
        if isinstance(data, list):
            api_array_list.append(data[0]['value'])
        else:
            api_array_list.append(data)
    county_name = api_array_list[0]
    maxIndex_list = []
    warning_list = []
    for data in json.loads(hot.body)['data']:
        if data['county'] == county_name:
            for towns in data['data']:
                maxIndex_list.append(towns['data'][0]['maxIndex'])
                warning_list.append(towns['data'][0]['maxWarning'])
    
    warning = warning_list[maxIndex_list.index(max(maxIndex_list))]

    UVIndex = 0
    for data in json.loads(uv.body)['data']:
        if data['county'] == county_name:
            UVIndex = int(data['UVIndex'])

    if UVIndex < 2:
        UVLevel = "低量級"
    elif 3 <= UVIndex < 6:
        UVLevel = "中量級"
    elif 6 <= UVIndex < 8:
        UVLevel = "高量級"
    elif 8 <= UVIndex < 11:
        UVLevel = "過量級"
    elif 11 <= UVIndex :
        UVLevel = "危險級"
    # construct discord api necessity
    server_url = 'https://discord.com/api/webhooks/1162404320399085690/y6pNTIyURc4-ftZIicqF49uzwNTF70bRw_9D1QyVrmxzbwagnXXX-HNW2E6QvzUJVUVS'
    timestamp = datetime.now().isoformat()
    base_url = request.base_url

    avatar_url = f"{base_url}images/chiikawa_avatar.webp"
    thumbnail_url = f"{base_url}images/chiikawa_thumbnail.jpg"
    image_url = f"{base_url}images/chiikawa_footer.png"

    message = {
        'username': '第八組吉伊卡哇',
        'avatar_url': avatar_url,
        'embeds': [{
            'title': f"吉伊卡哇的{api_array_list[0]}今日氣象",
            'type': 'rich',
            'description': '要小心壞天氣與奇美拉',
            'timestamp': timestamp,
            'color': 1572632,
            'footer': {
                'text': 'by 聖鎧、書硯、宜群、陳昊'
            },
            'thumbnail': {
                'url': thumbnail_url,
                'height': 1000,
                'width': 1400
            },
            'author': {
                'name': '下禮拜三就是睡衣派對!',
                'icon_url': avatar_url
            },
            'fields': [
                {'name': '天  氣🌤️', 'value': api_array_list[1], 'inline': True},
                {'name': '降  雨🌧️', 'value': f"{api_array_list[5]}%", 'inline': True},
                {'name': '氣  溫🌡️', 'value': f"{api_array_list[3]}~{api_array_list[2]}℃", 'inline': True},
                {'name': '紫外線🕵️‍♀️', 'value': UVLevel, 'inline': True},
                {'name': '熱傷害🥵', 'value': warning, 'inline': True},
                {'name': '舒適度🧋', 'value': api_array_list[4], 'inline': True}
            ],
            'image': {
                'url': image_url,
                'height': 375,
                'width': 1250
            }
        }]
    }

    headers = {
        'Content-Type': 'application/json'
    }
    
    
    try:
      response = requests.post(
          f"{server_url}?wait=true", headers=headers, data=json.dumps(message))
      response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
      # Process successful response
      response_data = response.json()
      return JSONResponse(
        status_code = status.HTTP_200_OK,
        content= response_data
      )
    except (requests.exceptions.HTTPError, requests.exceptions.RequestException):
        return JSONResponse(
            status_code=response.status_code,
            content={
                'error': True,
                'message':response.text
            }
        )



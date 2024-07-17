from fastapi import *
from typing import Annotated
import requests
import json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .weather import get_weather_by_county

router = APIRouter()

@router.get("/api/send_discord_message")
async def discord_bot(request: Request, weather: Annotated[dict, Depends(lambda county_name='臺北市': get_weather_by_county(county_name))]):
    
    # get data from Depends
    api_array_list = []

    for data in weather.values():
        if isinstance(data, list):
            api_array_list.append(data[0]['value'])
        else:
            api_array_list.append(data)

    print(api_array_list)

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
                {'name': '紫外線🕵️‍♀️', 'value': 'UV', 'inline': True},
                {'name': '熱傷害🥵', 'value': 'hotDam', 'inline': True},
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
      print("Response:", response_data)
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print('Response status code:', response.status_code)
        print('Response text:', response.text)

    except requests.exceptions.RequestException as req_err:
        print(f'Request exception occurred: {req_err}')



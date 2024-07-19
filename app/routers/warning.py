from fastapi import *
from fastapi.responses import JSONResponse
from config.basemodel import *
from pydantic import ValidationError
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import json

router = APIRouter(
    responses={
        400: {'model': Error, 'description': '資料取得失敗，輸入不正確或其他原因'},
        422: {'model': Error,
              'description': "輸入格式錯誤"
              },
        500: {'model': Error, 'description': '伺服器內部錯誤'}
    }
)

def fetch_hotindex():
  # clear the previous data
  global county_hot_damage_list
  county_hot_damage_list = []
  query_param = {
    "Authorization": "CWA-88EDF13E-87C9-4B54-B0A1-699275CFD8C2",
    "sort": "IssueTime"
    }
  url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/M-A0085-001"
  while county_hot_damage_list == []:
    data = requests.get(url, query_param).json()
    counties_data = data['records']['Locations']
    county_hot_damage = {}
    for county_data in counties_data:
      county_name = county_data['CountyName']
      town_hot_damage_list = []
      town_hot_damage = {}
      for town_data in county_data['Location']:
        town_name = town_data['TownName']
        hot_damage_list = []
        hot_damage = {}
        for time_data in town_data['Time']:
          date = time_data['IssueTime'].split(" ")[0]
          index = time_data['WeatherElements']['HeatInjuryIndex']
          warning = time_data['WeatherElements']['HeatInjuryWarning']
          if not hot_damage:
            hot_damage = {
              'date': date,
              'maxIndex': [index],
              'maxWarning': [warning]
            }
          elif hot_damage['date'] == date:
            hot_damage['maxIndex'].append(index)
            hot_damage['maxWarning'].append(warning)
          elif hot_damage['date'] != date:
            maxIndex = max(hot_damage['maxIndex'])
            ind = hot_damage['maxIndex'].index(maxIndex)
            hot_damage['maxIndex'] = maxIndex
            hot_damage['maxWarning'] = hot_damage['maxWarning'][ind]
            hot_damage_list.append(hot_damage)
            hot_damage = {
                'date': date,
                'maxIndex': [index],
                'maxWarning': [warning]
            }
        town_hot_damage = {
          'town': town_name,
          'data': hot_damage_list
        }
        town_hot_damage_list.append(town_hot_damage)
      county_hot_damage = {
        'county': county_name,
        'data': town_hot_damage_list
      }
      county_hot_damage_list.append(county_hot_damage)
    print('已取得氣象局熱傷害資料')

    dictionary = {'data': county_hot_damage_list}
    with open('warning.json', "w") as outfile:
      json.dump(dictionary, outfile)
      print('已將氣象局熱傷害資料存於json')

def station_id(id):
  match id:
    case "466850" | "466881" | "466900":
      return "新北市"
    case "466910"| "466920"| "466930":
      return "臺北市"
    case "466940"| '466950':
      return "基隆市"
    case "466990":
      return "花蓮縣"
    case "467050":
      return "桃園市"
    case "467080":
      return "宜蘭縣"
    case "467110":
      return "金門縣"
    case "467270":
      return "彰化縣"
    case "467280":
      return "苗栗縣"
    case "467300"| "467350":
      return "澎湖縣"
    case "467410"| "467420":
      return "臺南市"
    case "467441":
      return "高雄市"
    case "467480":
      return "嘉義市"
    case "467490":
      return "臺中市"
    case "467530":
      return "嘉義縣"
    case "467540"| "467610"| "467620"| "467660":
      return "臺東縣"
    case "467550"| "467650":
      return "南投縣"
    case "467571":
      return "新竹縣"
    case "467590"| "467790":
      return "屏東縣"
    case "467990":
      return "連江縣"

def fetch_uv():
  global county_UV_Index_list
  county_UV_Index_list = []
  query_param = {
      "Authorization": "CWA-88EDF13E-87C9-4B54-B0A1-699275CFD8C2"
  }
  url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0005-001"
  while county_UV_Index_list == []:
    data = requests.get(url, query_param).json()
    # Dictionary to store max UVIndex for each county
    max_uv_by_county = {}
    
    for location in data['records']['weatherElement']['location']:
      county = station_id(str(location['StationID']))
      uv_index = int(location['UVIndex'])
      if county not in max_uv_by_county or uv_index > max_uv_by_county[county]['UVIndex']:
        max_uv_by_county[county] = {
            'county': county,
            'UVIndex': uv_index
        }
    # Convert max_uv_by_county dictionary to a list of dictionaries
      county_UV_Index_list = list(max_uv_by_county.values())

    print('已取得氣象局紫外線資料')


# 中央氣象署每日下午 17:30 依據預測發布隔日之高溫資訊，並根據當日之最新預報及實際的高溫監測於 7: 30、11: 30、14: 30 定時更新


fetch_uv()
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_hotindex, 'cron', hour=8, minute=0)
scheduler.add_job(fetch_hotindex, 'cron', hour=12, minute=0)
scheduler.add_job(fetch_uv, 'cron', hour=14, minute=30)
scheduler.start()

@router.get("/api/hotdamage", responses={
  200: {'model': TaiwanHotDamage, 'description': "資料取得成功"}
},response_class=JSONResponse,summary="取得各縣市鄉鎮五天內當日最大熱傷害指數與傷害警示")
async def get_hot_damage(request: Request):
  try:
      content = {}
      if 'county_hot_damage_list' in globals():
        content = {'data': county_hot_damage_list}
        print("自global中取得熱傷害變數")
      else:
        with open('warning.json', "r") as readfile:
          content = json.load(readfile)
          print("自json中存取熱傷害資料")
      return JSONResponse(
          status_code=status.HTTP_200_OK,
          content=content
      )
  except (HTTPException, ValidationError) as e:
      response = Error(
          error=True,
          message=e.detail
      )
      return JSONResponse(
          status_code=e.status_code,
          content=dict(response)
      )


@router.get("/api/UV", responses={
  200: {'model': TaiwanUVIndex, 'description': "資料取得成功"}
},response_class=JSONResponse, summary="取得當日各縣市紫外線指數")
async def get_uv(request: Request):
  try:
    content = {'data': county_UV_Index_list}
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=content
    )
  except (HTTPException, ValidationError) as e:
      response = Error(
          error=True,
          message=e.detail
      )
      return JSONResponse(
          status_code=e.status_code,
          content=dict(response)
      )

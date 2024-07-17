from fastapi import *
from config.basemodel import *
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

router = APIRouter()

def fetch_hotindex():
  query_param = {
    "Authorization": "CWA-88EDF13E-87C9-4B54-B0A1-699275CFD8C2",
    "sort": "IssueTime"
    }
  url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/M-A0085-001"
  data = requests.get(url, query_param).json()
  counties_data = data['records']['Locations']
  county_hot_damage_list = []
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

  return {'data':county_hot_damage_list}

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
  query_param = {
      "Authorization": "CWA-88EDF13E-87C9-4B54-B0A1-699275CFD8C2"
  }
  url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0005-001"
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
  
  return {'data': county_UV_Index_list}


@router.get("/api/hotdamage", response_model=TaiwanHotDamage)
async def get_hot_damage(request: Request):
  return fetch_hotindex()


@router.get("/api/UV", response_model=TaiwanUVIndex)
async def get_uv(request: Request):
  return fetch_uv()
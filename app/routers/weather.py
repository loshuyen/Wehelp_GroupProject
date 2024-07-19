from fastapi import *
from config.basemodel import CurrentWeather, CountyWeather
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

router = APIRouter()

data1 = None
data2 = None
data1_active = False
data2_active = False

county_list = ["基隆市","臺北市","新北市","桃園市","新竹市","新竹縣","苗栗縣","臺中市","彰化縣","南投縣","雲林縣","嘉義市","嘉義縣","臺南市","高雄市","屏東縣","宜蘭縣","花蓮縣","臺東縣","澎湖縣","金門縣","連江縣"]

def fetchWeatherAll():
    query_param = {"Authorization": "CWA-88EDF13E-87C9-4B54-B0A1-699275CFD8C2"}
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    data = requests.get(url, query_param).json()
    locations = data["records"]["location"]
    return locations

def updateData():
    print("開始更新資料")
    global data1, data2, data1_active, data2_active
    if not data1_active and not data2_active:
        data1 = fetchWeatherAll()
        data1_active = True
    elif data1_active:
        data2 = fetchWeatherAll()
        data2_active = True
        data1_active = False
    else:
        data1 = fetchWeatherAll()
        data1_active = True
        data2_active = False
    print("結束更新資料")

def generate_publish_time(time):
    time_format = "%Y-%m-%d %H:%M:%S"
    time_obj = datetime.strptime(time, time_format)
    new_time_obj = time_obj - timedelta(hours=1)
    new_time_string = new_time_obj.strftime(time_format)
    return new_time_string

updateData()

scheduler = BackgroundScheduler()
scheduler.add_job(updateData, 'cron', hour=5, minute=30)
scheduler.add_job(updateData, 'cron', hour=11, minute=30)
scheduler.add_job(updateData, 'cron', hour=17, minute=30)
scheduler.add_job(updateData, 'cron', hour=23, minute=30)
scheduler.start()

@router.get("/api/weather")
def get_all_current_weather() -> CurrentWeather:
    try:
        data = data1 if data1_active else data2
        result = []
        publish_time = generate_publish_time(data[0]["weatherElement"][0]["time"][0]["startTime"])
        for index in range(len(county_list)):
            for i in data:
                if county_list[index] == i["locationName"]:
                    result.append(
                        {
                            "county": i["locationName"],
                            "Wx": i["weatherElement"][0]["time"][0]["parameter"]["parameterName"],
                            "PoP": i["weatherElement"][1]["time"][0]["parameter"]["parameterName"],
                            "MinT": i["weatherElement"][2]["time"][0]["parameter"]["parameterName"],
                            "CI": i["weatherElement"][3]["time"][0]["parameter"]["parameterName"],
                            "MaxT": i["weatherElement"][4]["time"][0]["parameter"]["parameterName"],
                        }
                    )
        return {"data": result, "publishTime": publish_time}
    except Exception as e:
        return e

@router.get("/api/weather/{county_name}")
def get_weather_by_county(county_name: str, factor: str | None = None) -> CountyWeather:
    try:
        data = data1 if data1_active else data2
        result = {
            "county": county_name,
            "Wx": None,
            "MaxT": None,
            "MinT": None,
            "CI": None,
            "PoP": None
        }
        for location in data:
            if location["locationName"] == county_name:
                data = location
                break
        if factor:
            for weather in data["weatherElement"]:
                if weather["elementName"] == factor:
                    data = weather
                    break
            arr = []
            for item in data["time"]:
                arr.append(
                    {
                        "startTime": item["startTime"],
                        "endTime": item["endTime"],
                        "value": item["parameter"]["parameterName"]
                    }
                )
            result[data["elementName"]] =  arr
        else:
            for weather in data["weatherElement"]:
                arr = []
                for time in weather["time"]:
                    arr.append(
                        {
                            "startTime": time["startTime"],
                            "endTime": time["endTime"],
                            "value": time["parameter"]["parameterName"]
                        }
                    )
                result[weather["elementName"]] = arr
        return result
    except Exception as e:
        return e
    
    
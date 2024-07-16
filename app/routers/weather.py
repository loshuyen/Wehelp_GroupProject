from fastapi import *
from config.basemodel import CurrentWeather, CountyWeather
import requests

router = APIRouter()

@router.get("/api/weather")
def get_all_current_weather() -> CurrentWeather:
    query_param = {"Authorization": "CWA-88EDF13E-87C9-4B54-B0A1-699275CFD8C2"}
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    data = requests.get(url, query_param).json()
    locations = data["records"]["location"]
    result = []
    for location in locations:
        result.append(
            {
                "county": location["locationName"],
                "Wx": location["weatherElement"][0]["time"][0]["parameter"]["parameterName"],
                "PoP": location["weatherElement"][1]["time"][0]["parameter"]["parameterName"],
                "MinT": location["weatherElement"][2]["time"][0]["parameter"]["parameterName"],
                "CI": location["weatherElement"][3]["time"][0]["parameter"]["parameterName"],
                "MaxT": location["weatherElement"][4]["time"][0]["parameter"]["parameterName"],
            }
        )
    return {"data": result}

@router.get("/api/weather/{county_name}")
def get_weather_by_county(county_name: str, factor: str | None = None) -> CountyWeather:
    auth_param = {
        "Authorization": "CWA-88EDF13E-87C9-4B54-B0A1-699275CFD8C2",
        "locationName": [f'{county_name}']
    }
    if factor:
        auth_param["elementName"] = factor
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    data = requests.get(url, auth_param).json()
    county_details = data["records"]["location"][0]
    items = county_details["weatherElement"]
    result = {
        "county": county_details["locationName"],
        "Wx": None,
        "MaxT": None,
        "MinT": None,
        "CI": None,
        "PoP": None
    }
    if factor:
        arr = []
        for i in items[0]["time"]:
            value = i["parameter"]["parameterName"]
            arr.append(
                {
                    "startTime": i["startTime"],
                    "endTime": i["endTime"],
                    "value": value
                }
            )
            result[items[0]["elementName"]] = arr
    else:
        for item in items:
            arr = []
            for i in item["time"]:
                value = i["parameter"]["parameterName"]
                arr.append(
                    {
                        "startTime": i["startTime"],
                        "endTime": i["endTime"],
                        "value": value
                    }
                )
                result[item["elementName"]] = arr
    return result

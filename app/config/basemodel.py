from pydantic import BaseModel

class CurrentWeatherBase(BaseModel):
    county: str
    Wx: str
    MaxT: int
    MinT: int
    CI: str
    PoP: int

class CurrentWeather(BaseModel):
    data: list[CurrentWeatherBase]
    publishTime: str

class WeatherBase(BaseModel):
    startTime: str
    endTime: str
    value: str

class ValueBase(WeatherBase):
    value: int

class CountyWeather(BaseModel):
    county: str
    Wx: list[WeatherBase] | None
    MaxT: list[ValueBase] | None
    MinT: list[ValueBase] | None
    CI: list[WeatherBase] | None
    PoP: list[ValueBase] | None
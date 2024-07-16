from pydantic import BaseModel

class CurrentWeatherBase(BaseModel):
    county: str
    wx: str
    max_t: int
    min_t: int
    ci: str
    pop: int

class CurrentWeather(BaseModel):
    data: list[CurrentWeatherBase]

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
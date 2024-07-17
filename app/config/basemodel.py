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


class HotDamage(BaseModel):
    date: str
    maxIndex: int
    maxWarning: str


class TownHotDamage(BaseModel):
    town: str
    data: list[HotDamage] | None


class CountyHotDamage(BaseModel):
    county: str
    data: list[TownHotDamage] | None


class TaiwanHotDamage(BaseModel):
    data: list[CountyHotDamage] | None


class CountyUVIndex(BaseModel):
    county: str
    UVIndex: int


class TaiwanUVIndex(BaseModel):
    data: list[CountyUVIndex]
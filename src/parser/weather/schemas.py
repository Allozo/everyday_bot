from pydantic import BaseModel


class WeatherHours(BaseModel):
    time: tuple[str, str]
    temperature: str
    status: str

    class Config:
        validate_assignment = True

    def __str__(self) -> str:
        return f"{':'.join(self.time):5} -- {self.temperature:>3} -- {self.status}"


class DailyWeather(BaseModel):
    town_name: str
    list_weather_hours: list[WeatherHours]

    class Config:
        validate_assignment = True

    def __str__(self) -> str:
        return "\n".join(
            [f"Погода в городе: {self.town_name}"]
            + [str(weather) for weather in self.list_weather_hours]
        )

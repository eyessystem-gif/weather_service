from __future__ import annotations

import json
from datetime import date
from urllib.parse import urlencode
from urllib.request import urlopen


CITY = "Seoul"
COUNTRY_CODE = "KR"


WEATHER_LABELS = {
    0: "맑음",
    1: "대체로 맑음",
    2: "부분적으로 흐림",
    3: "흐림",
    45: "안개",
    48: "서리 안개",
    51: "약한 이슬비",
    53: "이슬비",
    55: "강한 이슬비",
    61: "약한 비",
    63: "비",
    65: "강한 비",
    71: "약한 눈",
    73: "눈",
    75: "강한 눈",
    80: "약한 소나기",
    81: "소나기",
    82: "강한 소나기",
    95: "뇌우",
    96: "우박 동반 뇌우",
    99: "강한 우박 동반 뇌우",
}


def fetch_json(url: str, params: dict[str, str | int | float]) -> dict:
    request_url = f"{url}?{urlencode(params)}"
    with urlopen(request_url, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def geocode_city(city: str, country_code: str) -> dict:
    data = fetch_json(
        "https://geocoding-api.open-meteo.com/v1/search",
        {
            "name": city,
            "count": 10,
            "language": "ko",
            "format": "json",
        },
    )

    results = data.get("results", [])
    for result in results:
        if result.get("country_code") == country_code:
            return result

    if results:
        return results[0]

    raise ValueError(f"도시를 찾을 수 없습니다: {city}")


def get_today_hourly_weather(latitude: float, longitude: float) -> dict:
    return fetch_json(
        "https://api.open-meteo.com/v1/forecast",
        {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join(
                [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "precipitation_probability",
                    "precipitation",
                    "weather_code",
                    "wind_speed_10m",
                ]
            ),
            "forecast_days": 1,
            "timezone": "auto",
        },
    )


def main() -> None:
    location = geocode_city(CITY, COUNTRY_CODE)
    weather = get_today_hourly_weather(location["latitude"], location["longitude"])
    hourly = weather["hourly"]

    today = date.today().isoformat()
    print(f"{location['name']} 오늘 1시간 간격 날씨 ({today})")
    print("-" * 72)

    for index, time_text in enumerate(hourly["time"]):
        if not time_text.startswith(today):
            continue

        code = hourly["weather_code"][index]
        label = WEATHER_LABELS.get(code, f"알 수 없음({code})")

        print(
            f"{time_text[11:16]} | "
            f"{label:<10} | "
            f"기온 {hourly['temperature_2m'][index]:>5.1f}°C | "
            f"습도 {hourly['relative_humidity_2m'][index]:>3}% | "
            f"강수확률 {hourly['precipitation_probability'][index]:>3}% | "
            f"강수량 {hourly['precipitation'][index]:>4.1f}mm | "
            f"풍속 {hourly['wind_speed_10m'][index]:>4.1f}km/h"
        )


if __name__ == "__main__":
    main()

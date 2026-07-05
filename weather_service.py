from __future__ import annotations

import base64
import io
from datetime import datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from open_meteo_hourly_today import WEATHER_LABELS, fetch_json, get_today_hourly_weather


def geocode_location(query: str) -> dict:
    data = fetch_json(
        "https://geocoding-api.open-meteo.com/v1/search",
        {
            "name": query,
            "count": 1,
            "language": "ko",
            "format": "json",
        },
    )
    results = data.get("results", [])
    if not results:
        raise ValueError(f"Location not found: {query}")
    return results[0]


def collect_today_weather(query: str) -> dict:
    location = geocode_location(query)
    weather = get_today_hourly_weather(location["latitude"], location["longitude"])
    hourly = weather["hourly"]
    today = hourly["time"][0][:10]

    rows = []
    times = []
    temperatures = []

    for index, time_text in enumerate(hourly["time"]):
        if not time_text.startswith(today):
            continue

        temperature = hourly["temperature_2m"][index]
        weather_code = hourly["weather_code"][index]
        rows.append(
            {
                "time": time_text[11:16],
                "temperature": temperature,
                "humidity": hourly["relative_humidity_2m"][index],
                "precipitation_probability": hourly["precipitation_probability"][index],
                "precipitation": hourly["precipitation"][index],
                "wind_speed": hourly["wind_speed_10m"][index],
                "weather": WEATHER_LABELS.get(weather_code, f"Unknown ({weather_code})"),
            }
        )
        times.append(datetime.fromisoformat(time_text))
        temperatures.append(temperature)

    if not rows:
        raise RuntimeError("No hourly weather data found for today.")

    return {
        "location": {
            "name": location.get("name", query),
            "country": location.get("country", ""),
            "timezone": weather.get("timezone", ""),
            "latitude": location["latitude"],
            "longitude": location["longitude"],
        },
        "date": today,
        "summary": {
            "current": rows[0],
            "high": max(temperatures),
            "low": min(temperatures),
            "average": round(sum(temperatures) / len(temperatures), 1),
        },
        "hourly": rows,
        "graph": build_temperature_graph(times, temperatures, today),
    }


def build_temperature_graph(times: list[datetime], temperatures: list[float], today: str) -> str:
    fig, ax = plt.subplots(figsize=(11, 5.6))
    ax.plot(times, temperatures, marker="o", linewidth=2.4, color="#0f766e")
    ax.fill_between(times, temperatures, min(temperatures) - 1, color="#14b8a6", alpha=0.14)

    ax.set_title(f"Hourly Temperature - {today}")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (C)")
    ax.grid(True, linestyle="--", alpha=0.32)
    ax.set_xticks(times[::2])
    ax.set_xticklabels([time.strftime("%H:%M") for time in times[::2]], rotation=45)

    high_index = temperatures.index(max(temperatures))
    low_index = temperatures.index(min(temperatures))
    for label, index, offset in [("High", high_index, 12), ("Low", low_index, -18)]:
        ax.annotate(
            f"{label}: {temperatures[index]:.1f}C",
            xy=(times[index], temperatures[index]),
            xytext=(0, offset),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            color="#0f172a",
        )

    fig.tight_layout()
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=150)
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("ascii")

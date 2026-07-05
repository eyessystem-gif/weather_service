from __future__ import annotations

from datetime import date, datetime

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from open_meteo_hourly_today import COUNTRY_CODE, CITY, geocode_city, get_today_hourly_weather


OUTPUT_FILE = "today_temperature.png"


def main() -> None:
    location = geocode_city(CITY, COUNTRY_CODE)
    weather = get_today_hourly_weather(location["latitude"], location["longitude"])
    hourly = weather["hourly"]

    today = date.today().isoformat()
    times: list[datetime] = []
    temperatures: list[float] = []

    for time_text, temperature in zip(hourly["time"], hourly["temperature_2m"]):
        if time_text.startswith(today):
            times.append(datetime.fromisoformat(time_text))
            temperatures.append(temperature)

    if not times:
        raise RuntimeError(f"No hourly temperature data found for {today}.")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(times, temperatures, marker="o", linewidth=2.5, color="#2563eb")
    ax.fill_between(times, temperatures, min(temperatures) - 1, alpha=0.12, color="#2563eb")

    ax.set_title(f"Hourly Temperature Today - {CITY} ({today})")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (C)")
    ax.grid(True, linestyle="--", alpha=0.35)

    ax.set_xticks(times[::2])
    ax.set_xticklabels([time.strftime("%H:%M") for time in times[::2]], rotation=45)

    max_index = temperatures.index(max(temperatures))
    min_index = temperatures.index(min(temperatures))
    for label, index in [("High", max_index), ("Low", min_index)]:
        ax.annotate(
            f"{label}: {temperatures[index]:.1f}C",
            xy=(times[index], temperatures[index]),
            xytext=(0, 12 if label == "High" else -18),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            color="#111827",
        )

    fig.tight_layout()
    fig.savefig(OUTPUT_FILE, dpi=160)
    print(f"Saved graph: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

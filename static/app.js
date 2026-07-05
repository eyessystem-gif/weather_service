const form = document.querySelector("#weather-form");
const input = document.querySelector("#location-input");
const statusBox = document.querySelector("#status");
const result = document.querySelector("#result");
const submitButton = form.querySelector("button");

const currentTemp = document.querySelector("#current-temp");
const currentWeather = document.querySelector("#current-weather");
const highTemp = document.querySelector("#high-temp");
const lowTemp = document.querySelector("#low-temp");
const avgTemp = document.querySelector("#avg-temp");
const placeName = document.querySelector("#place-name");
const graph = document.querySelector("#temperature-graph");
const tableBody = document.querySelector("#hourly-table");

function formatTemp(value) {
  return `${Number(value).toFixed(1)}°C`;
}

function setStatus(message, isError = false) {
  statusBox.textContent = message;
  statusBox.classList.toggle("error", isError);
}

function renderWeather(data) {
  const locationText = [data.location.name, data.location.country].filter(Boolean).join(", ");
  currentTemp.textContent = formatTemp(data.summary.current.temperature);
  currentWeather.textContent = `${data.summary.current.time} · ${data.summary.current.weather}`;
  highTemp.textContent = formatTemp(data.summary.high);
  lowTemp.textContent = formatTemp(data.summary.low);
  avgTemp.textContent = formatTemp(data.summary.average);
  placeName.textContent = locationText;
  graph.src = `data:image/png;base64,${data.graph}`;

  tableBody.replaceChildren(
    ...data.hourly.map((row) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${row.time}</td>
        <td>${row.weather}</td>
        <td>${formatTemp(row.temperature)}</td>
        <td>${row.humidity}%</td>
        <td>${row.precipitation_probability}%</td>
        <td>${Number(row.wind_speed).toFixed(1)} km/h</td>
      `;
      return tr;
    }),
  );

  result.hidden = false;
  setStatus(`${locationText}의 ${data.date} 시간별 예보를 불러왔습니다.`);
}

async function loadWeather(location) {
  submitButton.disabled = true;
  result.hidden = true;
  setStatus("Open-Meteo에서 오늘 날씨를 불러오는 중입니다...");

  try {
    const response = await fetch(`/api/weather?location=${encodeURIComponent(location)}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "날씨 정보를 불러오지 못했습니다.");
    }

    renderWeather(data);
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    submitButton.disabled = false;
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  loadWeather(input.value.trim());
});

loadWeather(input.value.trim());

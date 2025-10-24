const fetchBtn = document.getElementById("fetchBtn");
const cityInput = document.getElementById("cityInput");
const display = document.getElementById("weatherDisplay");
const intervalSeconds = 60; // auto-refresh interval in seconds
document.getElementById("intervalSeconds").innerText = intervalSeconds;

let currentCity = null;
let autoTimer = null;

fetchBtn.addEventListener("click", () => {
  const city = cityInput.value.trim();
  if (!city) {
    display.innerHTML = `<p class="text-red-300">⚠️ Please enter a city name.</p>`;
    return;
  }
  currentCity = city;
  fetchAndShow(city);
  resetAutoRefresh();
});

function resetAutoRefresh() {
  if (autoTimer) clearInterval(autoTimer);
  autoTimer = setInterval(() => {
    if (currentCity) fetchAndShow(currentCity);
  }, intervalSeconds * 1000);
}

async function fetchAndShow(city) {
  display.innerHTML = `<p class="animate-pulse text-gray-200">Loading weather data...</p>`;
  try {
    const res = await fetch(`/weather?city=${encodeURIComponent(city)}`);
    const data = await res.json();
    if (!res.ok) {
      display.innerHTML = `
        <p class="text-red-300 font-semibold">❌ Error: ${data.error || "Unknown error"}</p>
        <pre class="text-gray-300 text-xs mt-2">${JSON.stringify(data.details || data, null, 2)}</pre>`;
      return;
    }
    showWeather(data);
  } catch (err) {
    display.innerHTML = `<p class="text-red-300">🌐 Network error: ${err.message}</p>`;
  }
}

function showWeather(d) {
  const iconUrl = d.icon
    ? `https://openweathermap.org/img/wn/${d.icon}@2x.png`
    : "";
  display.innerHTML = `
    <div class="fade-in">
      <div class="text-2xl font-semibold mb-1">
        ${d.city}${d.country ? ", " + d.country : ""}
      </div>
      ${iconUrl ? `<img src="${iconUrl}" alt="icon" class="mx-auto my-2 w-20 h-20">` : ""}
      <div class="text-lg mb-1">${d.description ?? ""}</div>
      <div>🌡 <strong>${d.temp ?? "—"}°C</strong> (Feels like ${d.feels_like ?? "—"}°C)</div>
      <div>💧 Humidity: ${d.humidity ?? "—"}%</div>
      <div>💨 Wind: ${d.wind_speed ?? "—"} m/s</div>
      <div class="text-xs text-gray-300 mt-2">
        Last updated: ${new Date().toLocaleTimeString()}
      </div>
    </div>
  `;
}


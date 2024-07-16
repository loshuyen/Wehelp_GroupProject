document.addEventListener("DOMContentLoaded", () => {
  const fetchWeatherData = async () => {
    try {
      const response = await fetch("/api/weather", {
        method: "GET",
      });
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching weather data:", error);
    }
  };
  const renderWeatherData = async () => {
    try {
      const data = await fetchWeatherData();
      const weatherTable = document.querySelector(".container-weather-table");

      if (!data || !data.data || data.data.length === 0) {
        const div = document.createElement("div");
        div.textContent = "No weather data available.";
        weatherTable.appendChild(div);
        return;
      }

      weatherTable.innerHTML = "";

      for (let i = 0; i < data.data.length; i++) {
        const weatherData = data.data[i];

        if (i % 2 === 0) {
          var rowDiv = document.createElement("div");
          rowDiv.className = "row";
        }

        const countyDiv = document.createElement("div");
        countyDiv.innerHTML = `
          <span>${weatherData.county}</span>
          <span>${weatherData.MinT}-${weatherData.MaxT}˚C</span>
          <span>${weatherData.PoP}%</span>
        `;

        rowDiv.appendChild(countyDiv);

        //last item or the next item starts a new row
        if (i === data.data.length - 1 || (i + 1) % 2 === 0) {
          weatherTable.appendChild(rowDiv);
        }
      }
    } catch (error) {
      console.error("Error rendering weather data:", error);
    }
  };

  renderWeatherData();
});

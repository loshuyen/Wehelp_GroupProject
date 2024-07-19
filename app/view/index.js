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

  async function sendDiscordMessage(countyName) {
    const url = new URL(window.location.href);
    url.pathname = "/api/send_discord_message";
    const params = { county_name: countyName };
    url.search = new URLSearchParams(params).toString();
    console.log(url);
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log("Response Data:", data);
    } catch (error) {
      console.error("Error:", error);
    }
  }

  const renderWeatherData = async () => {
    try {
      const data = await fetchWeatherData();
      const weatherTable = document.querySelector(".weather-table-content");

      const publishTimeDiv = document.querySelector(".all-county-publish-time");
      publishTimeDiv.innerHTML = `<p>發佈時間：${data.publishTime}</p>`;

      if (!data || !data.data || data.data.length === 0) {
        const div = document.createElement("div");
        div.textContent = "No weather data available.";
        weatherTable.appendChild(div);
        return;
      }

      for (let i = 0; i < data.data.length; i++) {
        const weatherData = data.data[i];

        if (i % 2 === 0) {
          var rowDiv = document.createElement("div");
          rowDiv.className = "row";
        }

        const countyDiv = document.createElement("div");
        countyDiv.className = "table-county-div";
        countyDiv.id = `county-${i}`;
        countyDiv.title = `${weatherData.Wx}`;

        countyDiv.innerHTML = `
          <span class="county-name">${weatherData.county}</span>
          <span>${weatherData.MinT}-${weatherData.MaxT}˚C</span>
          <div class="rain-pop"><span><img class="umbrella-icon" src="/images/umbrella.png" alt="">${weatherData.PoP}%</span></div>
          <img class="discord-icon" src="/images/chiikawa_avatar.webp" title="點我點我">
        `;
        const countyNameSpan = countyDiv.querySelector(".county-name");
        countyNameSpan.addEventListener("click", () => {
          window.location.href = `/county?name=${weatherData.county}`;
        });

        const discordIcon = countyDiv.querySelector(".discord-icon");
        discordIcon.addEventListener("click", () => {
          sendDiscordMessage(weatherData.county);
        });

        rowDiv.appendChild(countyDiv);

        if (i === data.data.length - 1 || (i + 1) % 2 === 0) {
          weatherTable.appendChild(rowDiv);
        }

        let svgRegion = document.getElementById(`svg-${i}`);

        if (svgRegion) {
          svgRegion.addEventListener("mouseenter", function () {
            svgRegion.querySelector("path").classList.add("highlight");
            countyDiv.classList.add("highlight");
          });

          svgRegion.addEventListener("mouseleave", function () {
            svgRegion.querySelector("path").classList.remove("highlight");
            countyDiv.classList.remove("highlight");
          });

          countyDiv.addEventListener("mouseenter", function () {
            svgRegion.querySelector("path").classList.add("highlight");
            countyDiv.classList.add("highlight");
          });

          countyDiv.addEventListener("mouseleave", function () {
            svgRegion.querySelector("path").classList.remove("highlight");
            countyDiv.classList.remove("highlight");
          });
        }
        svgRegion.addEventListener("click", () => {
          window.location.href = `/county?name=${weatherData.county}`;
        });
      }
    } catch (error) {
      console.error("Error rendering weather data:", error);
    }
  };

  const navWarningDiv = document.querySelector("#nav-warning");
  navWarningDiv.addEventListener("click", () => {
    window.location.href = "/warning";
  });

  renderWeatherData();
});

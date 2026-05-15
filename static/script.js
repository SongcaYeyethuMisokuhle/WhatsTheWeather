// Get the form from the HTML using its id
const weatherForm = document.getElementById("weatherForm");

// Get the input box where the user types the city name
const cityInput = document.getElementById("cityInput");

// Get the place where we will display the weather result
const weatherResult = document.getElementById("weatherResult");

// Listen for when the user submits the form
weatherForm.addEventListener("submit", async function (event) {
    // Stop the page from refreshing when the form is submitted
    event.preventDefault();

    // Get the city name typed by the user and remove extra spaces
    const city = cityInput.value.trim();

    // Check if the input is empty
    if (city === "") {
        weatherResult.innerHTML = `<p class="error">Please enter a city name.</p>`;
        return;
    }

    // Show a loading message while waiting for the backend response
    weatherResult.innerHTML = `<p>Loading weather...</p>`;

    try {
        // Send the city name to our FastAPI backend
        const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);

        // Convert the response from JSON text into a JavaScript object
        const data = await response.json();

        // If the backend returns an error, show the error message
        if (!response.ok) {
            weatherResult.innerHTML = `<p class="error">${data.detail || "Something went wrong."}</p>`;
            return;
        }

        // Display the real weather data on the page
        weatherResult.innerHTML = `
            <div class="weather-card">
                <h2>${data.city}, ${data.country}</h2>

                <p class="temperature">
                    ${data.temperature}${data.temperature_unit}
                </p>

                <p><strong>Humidity:</strong> ${data.humidity}%</p>

                <p><strong>Wind speed:</strong> ${data.wind_speed} ${data.wind_speed_unit}</p>

                <p><strong>Updated at:</strong> ${data.time}</p>

                <p class="summary">${data.summary}</p>
            </div>
        `;

    } catch (error) {
        // This runs if the frontend cannot connect to the backend
        weatherResult.innerHTML = `<p class="error">Could not connect to the server.</p>`;
    }
});
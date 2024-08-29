document
  .getElementById("getLocationLink")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Prevent the default link behavior

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
      document.getElementById("locationOutput").textContent =
        "Geolocation is not supported by this browser.";
    }
  });

function showPosition(position) {
  const latitude = position.coords.latitude;
  const longitude = position.coords.longitude;

  document.getElementById(
    "locationOutput"
  ).textContent = `Latitude: ${latitude}, Longitude: ${longitude}`;

  // Example: Redirect to a URL with the latitude and longitude as parameters
  // window.location.href = `https://example.com/?lat=${latitude}&long=${longitude}`;
}

function showError(error) {
  switch (error.code) {
    case error.PERMISSION_DENIED:
      document.getElementById("locationOutput").textContent =
        "User denied the request for Geolocation.";
      break;
    case error.POSITION_UNAVAILABLE:
      document.getElementById("locationOutput").textContent =
        "Location information is unavailable.";
      break;
    case error.TIMEOUT:
      document.getElementById("locationOutput").textContent =
        "The request to get user location timed out.";
      break;
    case error.UNKNOWN_ERROR:
      document.getElementById("locationOutput").textContent =
        "An unknown error occurred.";
      break;
  }
}

from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

OPENMETEO_API_BASE = "https://api.open-meteo.com/v1"
GEOCODING_API_BASE = "https://geocoding-api.open-meteo.com/v1"
USER_AGENT = "ktdreyer-weather-app/1.0"


# Helper function to make a request to the Open-Meteo API
async def make_openmeteo_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Open-Meteo API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


@mcp.tool()
async def get_current_weather(latitude: float, longitude: float) -> dict:
    """Get current weather for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """

    url = f"{OPENMETEO_API_BASE}/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,is_day,showers,cloud_cover,wind_speed_10m,wind_direction_10m,pressure_msl,snowfall,precipitation,relative_humidity_2m,apparent_temperature,rain,weather_code,surface_pressure,wind_gusts_10m&wind_speed_unit=mph&temperature_unit=fahrenheit&precipitation_unit=inch"

    data = await make_openmeteo_request(url)

    if not data:
        return "Unable to fetch current weather data for this location."

    return data


@mcp.tool()
async def search_location(name: str, count: int = 10) -> dict:
    """Search for a location by name to get coordinates.

    Args:
        name: Name of the city or location to search for
        count: Maximum number of results to return (default: 10)
    """

    url = f"{GEOCODING_API_BASE}/search?name={name}&count={count}&language=en&format=json"

    data = await make_openmeteo_request(url)

    if not data:
        return "Unable to fetch location data."

    return data


if __name__ == "__main__":
    # Initialize and run the server
    # For use with MCP clients inline:
    # mcp.run(transport='stdio')
    # For use with MCP clients "remotely", over http:
    mcp.run(transport='streamable-http')

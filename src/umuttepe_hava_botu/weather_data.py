import requests

UMUTTEPE_WEATHER_API_URL = "https://umuttepe-hava.vercel.app/api/weather"


def get_weather_data() -> str:
    r = requests.get(UMUTTEPE_WEATHER_API_URL)
    r.raise_for_status()
    data = r.json()
    summary: str = data["summary"]

    return summary

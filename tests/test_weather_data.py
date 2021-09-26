from umuttepe_hava_botu.weather_data import WeatherComParser

def test_weather_text():
    assert isinstance(WeatherComParser().get_weather_text(), str) == True

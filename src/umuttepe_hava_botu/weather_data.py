import requests
from bs4 import BeautifulSoup
from typing import Final


class WeatherComTurkishTranslation:
    MOSTLY_CLEAR_NIGHT: Final[str] = "Az Bulutlu"
    ORTA: Final[str] = "Az Bulutlu"  # Turkish
    PARTLY_CLOUDY_NIGHT: Final[str] = "Parçalı Bulutlu"
    PARTLY_CLOUDY: Final[str] = "Parçalı Bulutlu"
    SUNNY: Final[str] = "Güneşli"
    MOSTLY_SUNNY: Final[str] = "Çoğunlukla Güneşli"
    CLEAR_NIGHT: Final[str] = "Açık"

    @staticmethod
    def get_keys():
        translation = WeatherComTurkishTranslation()
        keys = [attr.replace('_', ' ').lower().title() for attr in dir(
            translation) if not callable(getattr(translation, attr)) and not attr.startswith("__")]
        return keys

    @staticmethod
    def get_translation(key: str):
        return getattr(WeatherComTurkishTranslation, key.replace(' ', '_').upper())


class WeatherComParser:

    UMUTTEPE_WEATHERCOM_URL: Final[str] = "https://weather.com/tr-TR/weather/today/l/c027c79a77e75cf682f052d9717291cc7ec6f677db4429eed536b950608f171d"

    def __init__(self) -> None:
        r = requests.get(self.UMUTTEPE_WEATHERCOM_URL)
        soup = BeautifulSoup(r.content, 'html.parser')

        self.current_temp: int = int(soup.select_one(
            'span.CurrentConditions--tempValue--3a50n').text.replace('°', '').strip())

        self.phrase_text: str = soup.select_one(
            'div.CurrentConditions--phraseValue--2Z18W').text.strip()

        if self.phrase_text in WeatherComTurkishTranslation.get_keys():
            self.phrase_text = WeatherComTurkishTranslation.get_translation(
                self.phrase_text)

        self.precip_text: str = ""

        self.precip_element = soup.select_one(
            'div.CurrentConditions--precipValue--3nxCj span')

        if self.precip_element:
            self.precip_text = self.precip_element.text.strip()

        self.later_element_sibling = soup.select_one(
            'div.TodayWeatherCard--TableWrapper--2kEPM ul.WeatherTable--wide--3dFXu li.Column--active--3vpgg')
        self.later_element = self.later_element_sibling.find_next_sibling(
            'li')
        if self.later_element is None:
            pass
            # TODO Hour by hour
            # https://weather.com/tr-TR/weather/hourbyhour/l/c027c79a77e75cf682f052d9717291cc7ec6f677db4429eed536b950608f171d

        if self.later_element:
            phrase_key = self.later_element.select_one('svg title').text
            self.later_phrase_text = None
            if phrase_key in WeatherComTurkishTranslation.get_keys():
                self.later_phrase_text = WeatherComTurkishTranslation.get_translation(
                    phrase_key)

            self.later_label = self.later_element.select_one(
                'h3').text
            self.later_temp = int(self.later_element.select_one(
                'div.Column--temp--5hqI_ span').text.replace('°', '').strip())

    def get_weather_text(self) -> str:
        text_all = f"Umuttepe'de hava şu an {self.phrase_text.lower()}, sıcaklık yaklaşık {self.current_temp}°C."

        if self.precip_text:
            text_all = text_all + f" {self.precip_text} bulunuyor."

        if self.later_element:
            text_all = text_all + \
                f" {self.later_label} hava {self.later_phrase_text.lower()}, tahmini sıcaklık {self.later_temp}°C."

        return text_all

# Importing libraries
import requests
import argparse
from bs4 import BeautifulSoup
from time import time, ctime
from math import ceil, floor


# Creating class for parser
class WeatherParser:
    def __init__(self):
        # Initializing constants
        self.HOST = 'https://sinoptik.ua/'
        self.HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'accept-language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'}
        self.ACTUALITY = 1 * 60 * 60

        # Initializing html variable for future manipulations
        self.html = None

    # Function for requests html
    def get_html(self, city=None, params=''):
        try:
            # Trying to parse site. If we have city using it to parse.
            if city:
                r = requests.get(f'{self.HOST}/погода-{city}/', headers=self.HEADERS, params=params)
            else:
                r = requests.get(self.HOST, headers=self.HEADERS, params=params)
        except requests.exceptions.ConnectionError:
            # Raise error if connection error
            raise ConnectionError("Check your internet connection!")
        else:
            # Else return html
            self.html = r
            return r

    # Parsing body
    def get_content(self):
        # Looking for html
        if self.html is None:
            raise TypeError("Have not HTML code! Run get_html before get_content.")

        # Creating parsers object
        soup = BeautifulSoup(self.html.text, 'html.parser')
        # Parsing weather
        items = soup.find_all('div', class_='main')
        # All results we will store in list
        weather_data = []

        for item in items:
            try:
                # First 3 boxes have <p class='day-link'>
                # But next boxes have <a class='day-link'>
                # So I use try constructions to avoid exception
                weather_data.append(
                    {
                        'weekday': item.find('p', class_='day-link').get_text(),
                        'date': item.find('p', class_='date').get_text(),
                        'month': item.find('p', class_='month').get_text(),
                        'weather': item.find('div', class_='weatherIco').get('title'),
                        'min_temp': item.find('div', class_='min').get_text()[5:],
                        'max_temp': item.find('div', class_='max').get_text()[6:]
                    }
                )
            except AttributeError:
                weather_data.append(
                    {
                        'weekday': item.find('a', class_='day-link').get_text(),
                        'date': item.find('p', class_='date').get_text(),
                        'month': item.find('p', class_='month').get_text(),
                        'weather': item.find('div', class_='weatherIco').get('title'),
                        'min_temp': item.find('div', class_='min').get_text()[5:],
                        'max_temp': item.find('div', class_='max').get_text()[6:]
                    }
                )
        # Inserting headers on top of list
        weather_data.insert(0, floor(time()))
        weather_data.insert(1, soup.find('div', class_='cityName').get_text()[2:])
        # Returning list
        return weather_data

    # Function those checks actuality of parsed information
    # It can be useful if program stores prevision results of parsing
    # But I discard this idea but leaved this method alone :D
    def is_actual(self, weather_data):
        weather_data_time = weather_data[0]
        if ceil(time()) - weather_data_time > self.ACTUALITY:
            return False
        return True


# Function those create args parser to handle users parameters
def create_args_parser():
    local_parser = argparse.ArgumentParser()
    local_parser.add_argument('-t', '--today', action='store_true', default=True)
    local_parser.add_argument('-w', '--week', action='store_true', default=False)
    local_parser.add_argument('-c', '--city', default=None)

    return local_parser


if __name__ == '__main__':
    # Creating args parser
    args_parser = create_args_parser()
    # Parsing args
    namespace = args_parser.parse_args()

    # Creating weather parser exemplar
    weather_parser = WeatherParser()
    # Getting html and pass parameters from args
    # Getting html code and handle excepts error
    html_code = weather_parser.get_html(city=namespace.city).status_code
    if html_code == 404:
        print(f'Not city named {namespace.city} founded!')
        exit(2)
    elif html_code != 200:
        print(f'Unidentified error (code: {html_code})!')
        exit(1)
    else:
        # Getting parsed information
        weather = weather_parser.get_content()

        # Printing information about parse time and city
        print(f'Parsed {ctime(weather[0])}', weather[1], '', sep='\n')

        # Handle parsed information
        if namespace.week:
            for i in weather:
                if type(i) == dict:
                    print(f"{i['weekday']}, {i['date']} {i['month']}: {i['min_temp']} - {i['max_temp']}  {i['weather']}")
        elif namespace.today:
            print(f"{weather[2]['weekday']}, {weather[2]['date']} {weather[2]['month']}: {weather[2]['min_temp']} - {weather[2]['max_temp']}  {weather[2]['weather']}")

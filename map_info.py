# BUS 216F-1: Python and Applications to Business Analytics II
# Yutong Li
# Part of the code is quoted from BUS216 Professor Namini's class notes

import json
import pandas as pd
import requests as re
from city import City
from datetime import datetime


class GIS:
    """
    This class contains data from the json file and get info about cities
    """

    data = 'city.list.json'

    with open(data) as json_file:
        # city_list: a Class attribute with city info
        city_list = json.load(json_file)

    # This method can get a list containing all the country names in the file
    @classmethod
    def get_countries_names(cls):
        country_list = []
        for c in cls.city_list:
            if c["country"] not in country_list and c['country'] != '':
                country_list.append(c["country"])

        return country_list

    # This method will get all city objects (or city objects in a specific country)
    @classmethod
    def get_cities_by_country(cls, country_list):
        """
        :param country_list: a list of country names
        :return: a dictionary of city info; key: city name; value: an city object
        """
        cities = []

        if country_list:
            for c in cls.city_list:
                if c['country'] in country_list:
                    # create a city object
                    city = City(c['id'], c['name'], c['state'], c['country'],
                                c['coord']['lon'], c['coord']['lat'])
                    cities.append(city)

        return cities

    @classmethod
    def get_us_states(cls):
        state_list = []
        for c in cls.city_list:
            if c['country'] == 'US' and c['state'] not in state_list and c['state'] != '':
                state_list.append(c['state'])
        return state_list

    @classmethod
    def get_cities_by_us_states(cls, state_list):
        """
        :param state_list: a list of state names
        :return: a dictionary of city info in the states
        """

        cities = []
        if state_list:
            for c in cls.city_list:
                if c['country'] == 'US' and c['state'] in state_list:
                    city = City(c['id'], c['name'], c['state'], c['country'],
                                c['coord']['lon'], c['coord']['lat'])
                    cities.append(city)
        return cities

    @classmethod
    def get_weather_info(cls, cities, open_weather_obj):
        """
        This function will return a dictionary containing each city's information
        :param open_weather_obj: an object of open weather
        :param cities: a list of city object
        :return: a dataframe containing city information
        """

        # Create an empty list to store city information dictionaries
        weather_info = []

        for i in range(len(cities)):
            try:
                r_as_json = open_weather_obj.execute(cities[i].name, should_print=True)

                ts = r_as_json['dt']
                time = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                temp = r_as_json['main']['temp']
                humidity = r_as_json['main']['humidity']
                wind_speed = r_as_json['wind']['speed']
                lon = r_as_json["coord"]["lon"]
                lat = r_as_json["coord"]["lat"]
                weather_info.append(
                    {"City": cities[i].name,
                     "Country": cities[i].country,
                     "Temperature": temp,
                     "Humidity": humidity,
                     "Wind_Speed": wind_speed,
                     "Datetime": time,
                     "Longitude": lon,
                     "Latitude": lat})

            except KeyError as e:
                print(e)
            except re.exceptions.RequestException as e:
                print(e)
                raise SystemExit(e)
            except OSError as e:
                print(e)

        # create a dataframe for weather_info
        weather_info_df = pd.DataFrame(weather_info)
        return weather_info_df

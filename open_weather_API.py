# BUS 216F-1: Python and Applications to Business Analytics II
# Yutong Li
# This code is quoted from BUS216 Professor Namini's notes

# import libraries
import json
import requests as re


class OpenWeather:
    """
    documentation = https://openweathermap.org/current
    """
    endpoint_template = 'http://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}&mode={mode}&units={units}'
    api_key = '5f458dfbcfd21a1f81b3b6e744c5522e'

    def __init__(self):
        """
         This is the constructor for this class
         endpoint: the API endpoint
         """
        self.endpoint = OpenWeather.endpoint_template.replace('{API key}', OpenWeather.api_key)

    def execute(self, city, should_print=False, mode='json', units='imperial'):
        """
        This is the execute function for the class
        :return r_as_json: a json dictionary
        """

        endpoint = self.endpoint.replace('{city name}', city)
        endpoint = endpoint.replace('{mode}', mode)
        endpoint = endpoint.replace('{units}', units)

        r = re.get(endpoint)
        if mode == 'json':
            r_as_json = json.loads(r.text)
            if should_print:
                print(json.dumps(r_as_json, indent=2))
            return r_as_json
        elif mode == 'xml':
            pass
        elif mode == 'html':
            pass
        else:
            if should_print:
                print(r.text)

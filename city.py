# BUS 216F-1: Python and Applications to Business Analytics II
# Yutong Li
# This code is quoted from BUS216 Professor Namini's class notes

class City:

    def __init__(self, id, name, state, country, longitude, latitude):
        """
        This is the constructor for this class
        """
        self.id = id
        self.name = name
        self.state = state
        self.country = country
        self.longitude = float(longitude)
        self.latitude = float(latitude)

    def __str__(self):
        return f'{self.id}:{self.name}:{self.state}:{self.country}:{self.longitude}:{self.latitude}'


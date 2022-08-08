from datetime import datetime
from config import TIME_TOKEN
import requests
from pprint import pprint

#
# lat = 55.751244
# lon = 37.618423
# # url = 'https://api.ipgeolocation.io/timezone?apiKey=API_KEY&lat=-27.4748&long=153.017'
# r = requests.get(f'https://api.ipgeolocation.io/timezone?apiKey={TIME_TOKEN}&lat={lat}&long={lon}')
# data = r.json()
# pprint(data)
# print('---------')
# lat2 = 51.509865
# lon2 = -0.118092
# r = requests.get(f'https://api.ipgeolocation.io/timezone?apiKey={TIME_TOKEN}&lat={lat2}&long={lon2}')
# data = r.json()
# pprint(data)
#
# lat3 = 36.778259
# lon3 = -119.417931
# print('---------')
# r = requests.get(f'https://api.ipgeolocation.io/timezone?apiKey={TIME_TOKEN}&lat={lat3}&long={lon3}')
# data = r.json()
# pprint(data)

def get_timezone(location, token=TIME_TOKEN):
    lat = float(location[0])
    lon = float(location[1])
    r = requests.get(f'https://api.ipgeolocation.io/timezone?apiKey={TIME_TOKEN}&lat={lat}&long={lon}')
    data = r.json()
    return data['timezone_offset']


locat = [36.778259, -119.417931]


print(get_timezone(locat))
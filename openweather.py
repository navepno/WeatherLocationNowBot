from config import WEATHER_TOKEN
from pprint import pprint
import requests
from datetime import datetime

# current_date = datetime.now()
# print(current_date.strftime('%d.%m.%Y'))

city = 'липецк'
limit = 5
country = 'RU'
r = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit={limit}&appid={WEATHER_TOKEN}')
data = r.json()
pprint(data)
# for i in data:
#     print('------')
#     pprint(i)
# pprint(data[0])

# def get_weather(location, token):
#     try:
#         lat = float(location[0])
#         lon = float(location[1])
#         r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token}&lang=ru&units=metric')
#         data = r.json()
#         pprint(data)
#         current_date = datetime.now()
#         # pprint(data['main']['feels_like'])
#         output = f'Погода на {current_date.strftime("%d.%m.%Y")}\n' \
#                          f'Температура: {data["main"]["temp"]}°C, {data["weather"][0]["description"]}\n' \
#                          f'Ощущается как: {data["main"]["feels_like"]}°C\n' \
#                          f'Ветер {data["wind"]["speed"]}м/с'
#         return output
#     except Exception as ex:
#         print(ex)
#         print("incorrect location")
#
#
# moscow = ['55.751244', '37.618423']

# print(get_weather(moscow, WEATHER_TOKEN))

# output = f'Погода на {current_date.strftime("%d.%m.%Y")}\n' \
#                  f'Температура: {data["main"]["temp"]}°C, {data["weather"]["description"]}\n' \
#                  f'Ощущается как: {data["feels_like"]}°C\n' \
#                  f'Ветер {data["wind"]["speed"]}м/с'
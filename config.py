import psycopg2


TOKEN = '5372678427:AAGph4JP1aQGEWJXtcphqN0nlAPO1ZieF5Y'
WEATHER_TOKEN = '19559775c4c4a70f132acfc61d5687bc'
TIME_TOKEN = '4aeca68742a94b87b7fd7f53ebe63c7e'

CONNECTION = psycopg2.connect(
    dbname='Weather_db',
    user='navepno',
    password='9051',
    host='localhost'
)

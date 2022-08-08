import psycopg2
from config import CONNECTION
import db

test = 'test'

first = {'chat_id': 2134,
         'username': 'navepnoe',
         'timezone_offset': '3'}


db.insert(first)


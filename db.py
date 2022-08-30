import psycopg2
from config import CONNECTION

#
# chat_id = '12345'
# username = 'navepno'
# latitude = '52.12'
# longitude = '23.45'

# conn = CONNECTION
# cursor = conn.cursor()


def insert(column_values, table='userweatherbot'):
    conn = CONNECTION
    cursor = conn.cursor()
    columns = ', '.join(column_values.keys())
    print(columns)
    values = tuple(column_values.values())
    placeholders = ''
    for i in range(3):
        placeholders += '%s, '
    placeholders = placeholders[:len(placeholders) - 2]
    cursor.execute(f'INSERT INTO {table}'
                   f'({columns}) '
                   f'VALUES ({placeholders})',
                   values)
    conn.commit()
    cursor.close()
    conn.close()


# def get_cursor():
#     return cursor
#
#
# cursor.close()
# conn.close()

'''
НИЖЕ ПОМОЙКА
'''

# conn = psycopg2.connect(
#     dbname='navepno_db',
#     user='navepno',
#     password='9051',
#     host='localhost'
# )


# cursor = conn.cursor()

# cursor.execute("INSERT INTO userweatherbot (chat_id, username, latitude, longitude) VALUES (%s, %s, %s, %s)",
#                (chat_id, username, latitude, longitude))
# conn.commit()

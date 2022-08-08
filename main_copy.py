from config import TOKEN, WEATHER_TOKEN, TIME_TOKEN, CONNECTION
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, time
import requests
from pprint import pprint
import psycopg2
from bs4 import BeautifulSoup

bot = telebot.TeleBot(TOKEN)
conn = CONNECTION
user_dict = {}

'''
TODO
'''


class User:
    def __init__(self, name):
        self.name = name
        self.timezone_offset = None
        self.location = None
        self.time = None
        self.days = None


def get_lat_lon(city, token=WEATHER_TOKEN):
    try:
        limit = 3
        country = 'RU'
        r = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit={limit}&appid={WEATHER_TOKEN}')
        data = r.json()
        return data
    except Exception as ex:
        print(ex)
        print("incorrect location")


def get_weather(location, token=WEATHER_TOKEN):
    try:
        lat = float(location[0])
        lon = float(location[1])
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token}&lang=ru&units=metric')
        data = r.json()
        current_date = datetime.now()
        # pprint(data['main']['feels_like'])
        output = f'Погода на {current_date.strftime("%d.%m.%Y")}\n' \
                         f'Температура: {data["main"]["temp"]}°C, {data["weather"][0]["description"]}\n' \
                         f'Ощущается как: {data["main"]["feels_like"]}°C\n' \
                         f'Ветер {data["wind"]["speed"]}м/с'
        return output
    except Exception as ex:
        print(ex)
        print("incorrect location")


def get_timezone(location, token=TIME_TOKEN):
    lat = float(location[0])
    lon = float(location[1])
    r = requests.get(f'https://api.ipgeolocation.io/timezone?apiKey={TIME_TOKEN}&lat={lat}&long={lon}')
    data = r.json()
    return data['timezone_offset']


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Привет! \nЭтот бот может присылать тебе погоду в твоем городе каждый день в '
                                      'выбранное время \nМне нужны только время отправки погоды и твоя локация')
    bot.send_message(message.chat.id, 'Чем я могу помочь?')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                                          'Привет! \nЭтот бот может присылать тебе погоду в твоем городе каждый день в '
                                          'выбранное время \nМне нужны только время отправки погоды и твоя локация')
    chat_id = message.chat.id
    name = message.chat.username
    user = User(name)
    user_dict[chat_id] = user
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Кину свою локацию", callback_data="get_location"),
               InlineKeyboardButton("Кину название города", callback_data="get_city"))
    get_type_location = bot.send_message(chat_id, 'Ты хочешь поделиться геопозицией или названием города', reply_markup=markup)
    # bot.register_next_step_handler(get_type_location, location_or_city)


'''rename functions get choise'''


@bot.callback_query_handler(func=lambda call: call.data in ['get_location', 'get_city'])
def location_or_city(call: telebot.types.CallbackQuery):
    print(f'AAAAAAAAAAA {type(call)}')
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id, 'Загрузил в себя эту информацию')
    if call.data == 'get_location':
        location_markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_location = telebot.types.KeyboardButton('Отправить геолокацию', request_location=True)
        location_markup.add(button_location)
        text = bot.send_message(chat_id, 'Поделись своей геопозицией', reply_markup=location_markup)
        bot.register_next_step_handler(text, get_location_or_city)
    elif call.data == 'get_city':
        text = bot.send_message(chat_id, 'Напиши название города')
        bot.register_next_step_handler(text, get_location_or_city)


def get_location_or_city(message):
    chat_id = message.chat.id
    try:
        if message.text is None:
            user = user_dict[chat_id]
            location = [f'{message.location.latitude}', f'{message.location.longitude}']
            timezone_offset = get_timezone(location)
            user.location = location
            user.timezone_offset = timezone_offset
            stop_markup = telebot.types.ReplyKeyboardRemove()
            text = bot.send_message(chat_id, 'Напиши время, когда ты хочешь получать уведомления о погоде\n'
                                             'Пример: 08:21',
                                    reply_markup=stop_markup)
            # bot.register_next_step_handler(text, get_time_to_send)
            print(user.location)
        else:
            data = get_lat_lon(message.text)
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            location = [latitude, longitude]
            timezone_offset = get_timezone(location)
            user = user_dict[chat_id]
            user.location = location
            user.timezone_offset = timezone_offset
            yes_no_geo_markup = InlineKeyboardMarkup()
            yes_no_geo_markup.row_width = 1
            yes_no_geo_markup.add(InlineKeyboardButton('Да', callback_data="correct"),
                              InlineKeyboardButton('Нет', callback_data="incorrect"))
            bot.send_location(chat_id, latitude=latitude, longitude=longitude)
            bot.send_message(chat_id, 'Я правильно понял город?', reply_markup=yes_no_geo_markup)
    except Exception as ex:
        print(ex)
        location_markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_location = telebot.types.KeyboardButton('Отправить геолокацию', request_location=True)
        location_markup.add(button_location)
        exception_location = bot.send_message(chat_id, 'Я не нашел такого города\n'
                                  'Отправь, пожалуйста, геолокацию', reply_markup=location_markup)
        bot.register_next_step_handler(exception_location, get_location_or_city)


@bot.callback_query_handler(func=lambda call: call.data in ['correct', 'incorrect'])
def get_location_from_city(call: telebot.types.CallbackQuery):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id, 'Загрузил в себя эту информацию')
    if call.data == 'correct':
        stop_markup = telebot.types.ReplyKeyboardRemove()
        text = bot.send_message(chat_id, 'Напиши время, когда ты хочешь получать уведомления о погоде\n'
                                         'Пример: 08:21',
                                reply_markup=stop_markup)
        bot.register_next_step_handler(text, get_time_to_send)
    elif call.data == 'incorrect':
        location_markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_location = telebot.types.KeyboardButton('Отправить геолокацию', request_location=True)
        location_markup.add(button_location)
        get_location_again = bot.send_message(chat_id, 'Прости, я не понял где ты\n'
                                  'Отправь, пожалуйста, геолокацию', reply_markup=location_markup)
        bot.register_next_step_handler(get_location_again, get_location_or_city)


def get_time_to_send(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    time = message.text
    try:
        if ':' not in time:
            print(1)
            again = bot.send_message(chat_id, '1Неверный формат времени\nНапиши в формате: 08:21')
            bot.register_next_step_handler(again, get_time_to_send)
        elif len(time.split(':')) != 2:
            print(2)
            again = bot.send_message(chat_id, '2Неверный формат времени\nНапиши в формате: 08:21')
            bot.register_next_step_handler(again, get_time_to_send)
        elif not (0 <= int(time.split(':')[0]) < 24) or not (0 <= int(time.split(':')[1]) < 60):
            print(3)
            # elif (0 > int(time.split(':')[0]) >= 24) and (0 > int(time.split(':')[1]) >= 60):
            again = bot.send_message(chat_id, '3Неверный формат времени\nНапиши в формате: 08:21')
            bot.register_next_step_handler(again, get_time_to_send)
        else:
            print(4)
            user.time = message.text
            days_of_week_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота',
                                 'Воскресенье']
            poll = bot.send_poll(chat_id, 'Выберите дни недели', days_of_week_list,
                                 allows_multiple_answers=True,
                                 is_anonymous=False)
            # bot.register_next_step_handler(poll, get_days_to_send)

    except:
        again = bot.send_message(chat_id, '4Неверный формат времени\nНапиши в формате: 08:21')
        bot.register_next_step_handler(again, get_time_to_send)


@bot.poll_answer_handler(func=lambda call: True)
def get_days_to_send(call):
    print(f'11111 {type(call)}')
    chat_id = call.user.id
    # print(call)
    answers = {0: 'Понедельникам', 1: 'Вторникам', 2: 'Средам', 3: 'Четвергам',
               4: 'Пятницам', 5: 'Субботам', 6: 'Воскресеньям'}

    out = []
    user = user_dict[chat_id]
    user.days = call.option_ids
    for i in call.option_ids:
        if i in answers:
            out.append(answers[i])
    bot.send_message(call.user.id, f'Уведомления будут приходить в {user.time} по {", ".join(out)}')
    # bot.send_message(call.user.id, f'user -- {user.name}\n'
    #                                f'location -- {user.location}\n'
    #                                f'time -- {user.time}\n'
    #                                f'days -- {user.days}')
    yes_no_markup = InlineKeyboardMarkup()
    yes_no_markup.row_width = 1
    yes_no_markup.add(InlineKeyboardButton('Да', callback_data="yes"),
                      InlineKeyboardButton('Нет', callback_data="no"))
    end_or_no = bot.send_message(chat_id, 'Хочешь выбрать другое время с другими днями?', reply_markup=yes_no_markup)
    # bot.register_next_step_handler(end_or_no, get_end)


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def get_end(call):
    print(f'22222 {type(call)}')
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id, 'Загрузил в себя эту информацию')
    if call.data == 'yes':
        stop_markup = telebot.types.ReplyKeyboardRemove()
        text = bot.send_message(chat_id, 'Напиши время, когда ты хочешь получать уведомления о погоде',
                                reply_markup=stop_markup)
        bot.register_next_step_handler(text, get_time_to_send)
    elif call.data == 'no':
        stop_markup = telebot.types.ReplyKeyboardRemove()
        text = bot.send_message(chat_id, 'Хорошо, бот запущен!',
                                reply_markup=stop_markup)


@bot.message_handler(commands=['weather'])
def send_current_weather(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Текущая погода:')


@bot.message_handler(commands=['edit_location'])
def edit_location(message):
    pass


@bot.message_handler(commands=['edit_notifications'])
def edit_notifications(message):
    pass


@bot.message_handler(commands=['my_notifications'])
def get_my_notifications(message):
    pass


@bot.message_handler(commands=['weather_now'])
def get_weather_now(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    output_data = get_weather(user.location)
    bot.send_message(chat_id, output_data)




bot.infinity_polling()
# if __name__ == '__main__': # чтобы код выполнялся только при запуске в виде сценария, а не при импорте модуля
#     try:
#        bot.polling(none_stop=True) # запуск бота
#     except Exception as e:
#        print(e) # или import traceback; traceback.print_exc() для печати полной инфы
#        time.sleep(15)
'''
НИЖЕ ПОМОЙКА
'''
# @bot.message_handler(func=lambda message: True)
# def update_location(message):
#     text = bot.send_message(message.chat.id, 'Спасибо, что скинул город, а не локацию')
#     bot.register_next_step_handler(text, get_time_to_send)
#
#
# @bot.message_handler(content_types=['location'])
# def update_location(message):
#     text = bot.send_message(message.chat.id, message.chat.location)
#     bot.register_next_step_handler(text, get_time_to_send)

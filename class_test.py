
# class User:
#     def __init__(self, name):
#         self.name = name
#         self.timezone_offset = None
#         self.location = None
#         self.time = None
#         self.days = {
#             'Понедельник': '-',
#             'Вторник': '-',
#             'Среда': '-',
#             'Четверг': '-',
#             'Пятница': '-',
#             'Суббота': '-',
#             'Воскресенье': '-'
#         }
#
#
# bogdan = User('bog')
# bogdan.days['Вторник'] = 1
# print(bogdan.days)


days = {
            'Понедельник': '',
            'Вторник': '',
            'Среда': '',
            'Четверг': '3',
            'Пятница': '',
            'Суббота': '2',
            'Воскресенье': ''
        }

out = ''
for i in days:
    if days[i] != '':
        out += f'{i}: {days[i]}\n'


print(out)
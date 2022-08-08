# answers = {0: 'Понедельник', 1: 'Вторник', 2:'Среда', 3:'Четверг', 4:'Пятница', 5:'Суббота', 6:'Воскресенье'}
# lst = [3, 4]
# for i in lst:
#     if i in answers:
#         print(answers[i])
#

# s = '24:52'
# s2 = '08:34'
# print(int(s[:2]) in [0, 24])
#
# def format_time(s):
#
#     if ':' in s:
#         t = s.split(':')
#         print(t)
#         if len(t) == 2:
#             print(int(t[0]))
#             print(int(t[1]))
#             if 0 <= int(t[0]) < 24 and 0 <= int(t[1]) < 60:
#                 print('ok')
# print(format_time(s))



# elif (int(time.split(':')[0] not in hours) and (int(time.split(':')[1] not in minutes):

# hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
# minutes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
# hours = [i for i in range(24)]
# minutes = [i for i in range(60)]

# time = "12:343"
# if ((int(time.split(':')[0]) >= 24) or (int(time.split(':')[0]) < 0)) or ((int(time.split(':')[1]) >= 60) or (int(time.split(':')[1]) < 0)):
# # if (int(time.split(':')[0]) not in hours) and (int(time.split(':')[1]) not in minutes):
#     print((int(time.split(':')[0]) >= 24))
#     print((int(time.split(':')[0]) < 0))
#     print((int(time.split(':')[1]) >= 60))
#     print((int(time.split(':')[1]) < 0))
# else:
#     print('okay')
#     print((int(time.split(':')[0]) >= 24))
#     print((int(time.split(':')[0]) < 0))
#     print((int(time.split(':')[1]) >= 60))
#     print((int(time.split(':')[1]) < 0))


time = "12:34"
if not (0 <= int(time.split(':')[0]) < 24) or not (0 <= int(time.split(':')[1]) < 60):
    print('aaaa')
# if (int(time.split(':')[0]) not in hours) and (int(time.split(':')[1]) not in minutes):
    print((int(time.split(':')[0]) >= 24))
    print((int(time.split(':')[0]) < 0))
    print((int(time.split(':')[1]) >= 60))
    print((int(time.split(':')[1]) < 0))
else:
    # print('okay')
    print(0 > int(time.split(':')[0]) >= 24)
    print(not (0 > int(time.split(':')[1]) >= 60))
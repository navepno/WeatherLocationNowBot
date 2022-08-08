# placeholders = ', '.join('?' * 3)
# placeholders.replace('?', '%s')
# print(placeholders)

placeholders = ''
for i in range(3):
    placeholders += '%s, '
placeholders = placeholders[:len(placeholders) - 2]
print(placeholders)
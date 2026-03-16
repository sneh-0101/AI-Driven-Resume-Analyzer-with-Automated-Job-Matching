import sqlite3

conn = sqlite3.connect('instance/app.db')
cursor = conn.cursor()

cursor.execute('SELECT username, email, is_admin FROM users WHERE is_admin = 1')
admins = cursor.fetchall()

if admins:
    print('Existing admin users:')
    for admin in admins:
        print(f'  - {admin[0]} ({admin[1]})')
else:
    print('No admin users found.')

conn.close()

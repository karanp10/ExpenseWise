import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys = ON;')

cursor.execute('DROP TABLE IF EXISTS expenses')
cursor.execute('DROP TABLE IF EXISTS categories')
cursor.execute('DROP TABLE IF EXISTS budget')
cursor.execute('DROP TABLE IF EXISTS income')
cursor.execute('DROP TABLE IF EXISTS mandatory_expenses')
cursor.execute('DROP TABLE IF EXISTS groups')
cursor.execute('DROP TABLE IF EXISTS users')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS income (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      amount REAL,
      FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT UNIQUE
    )
''')

cursor.execute("INSERT INTO groups (name) VALUES ('Savings')")
cursor.execute("INSERT INTO groups (name) VALUES ('Necessities')")
cursor.execute("INSERT INTO groups (name) VALUES ('Luxuries')")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS mandatory_expenses (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      group_id INTEGER,
      name TEXT,
      amount REAL,
      FOREIGN KEY(user_id) REFERENCES users(id),
      FOREIGN KEY(group_id) REFERENCES groups(id) ON DELETE CASCADE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      name TEXT,
      FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      name TEXT,
      category_id INTEGER,
      category TEXT,
      amount REAL,
      date TEXT,
      FOREIGN KEY(user_id) REFERENCES users (id),
      FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE CASCADE
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      amount REAL,
      FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')
conn.commit()
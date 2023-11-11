import sqlite3

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS categories')
cursor.execute('DROP TABLE IF EXISTS expenses')
cursor.execute('DROP TABLE IF EXISTS budget')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT UNIQUE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      category_id INTEGER,
      category TEXT,
      amount REAL,
      date TEXT,
      FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE CASCADE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget (
      amount REAL
    )
''')
conn.commit()
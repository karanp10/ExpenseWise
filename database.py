import sqlite3

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
      name TEXT PRIMARY KEY
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
      name TEXT,
      category TEXT,
      amount REAL,
      FOREIGN KEY(category) REFERENCES categories(name) ON DELETE CASCADE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget (
      amount REAL
    )
''')
conn.commit()
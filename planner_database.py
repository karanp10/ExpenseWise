import sqlite3

conn = sqlite3.connect('budget.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS income')
cursor.execute('DROP TABLE IF EXISTS mandatory_expenses')
cursor.execute('DROP TABLE IF EXISTS categories')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS income (
      amount REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT UNIQUE
    )
''')

cursor.execute("INSERT INTO categories (name) VALUES ('Savings')")
cursor.execute("INSERT INTO categories (name) VALUES ('Necessities')")
cursor.execute("INSERT INTO categories (name) VALUES ('Luxuries')")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS mandatory_expenses (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      category_id INTEGER,
      name TEXT,
      amount REAL,
      FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE CASCADE
    )
''')

conn.commit()




import streamlit as st
import sqlite3
import bcrypt

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
conn.commit()


def check_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user is None:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8'))

def get_user_id(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user is not None:
        return user[0]
    else:
        return None
    
def create_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long'
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password.decode('utf-8')))
        conn.commit()
        return True, 'User created successfully'
    except sqlite3.IntegrityError:
        return False, 'Username is already taken'
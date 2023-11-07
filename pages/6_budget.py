import streamlit as st
import sqlite3


conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

def budget():
    cursor.execute('SELECT amount FROM budget')
    budget = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(amount) FROM expenses')
    expenses = cursor.fetchone()[0]
    if expenses is None:
        expenses = 0
    
    remaining = budget - expenses
    col1, col2 = st.columns([1,1])
    col1.metric(label='Budget', value=f'${budget}')
    col2.metric(label='Remaining', value=f"${remaining}", delta=f"${expenses - budget}")

st.set_page_config(page_title="budget", page_icon="📊")
budget()

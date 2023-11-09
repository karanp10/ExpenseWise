import streamlit as st
import sqlite3


conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()



def expense():
    cursor.execute('SELECT name FROM categories')
    categories = [category[0] for category in cursor.fetchall()]

    with st.form(key='expense_form'):
        name = st.text_input('Enter expense name')
        category = st.selectbox('Select category', categories)
        amount = st.number_input('Enter amount', min_value=0.0)
        submit_button = st.form_submit_button(label='Submit')
    
    if submit_button:
        cursor.execute('INSERT INTO expenses (name, category, amount) VALUES (?, ?, ?)', (name, category, amount))
        conn.commit()
        st.success('Expense added successfully!')

    cursor.execute('''
        SELECT expenses.name, expenses.category, expenses.amount 
        FROM expenses 
    ''')
    expenses = cursor.fetchall()

    for i, expense in enumerate(expenses):
        col1, col2, col3, col4 = st.columns([2,2,2,2])
        col1.text(expense[0])
        col2.text(expense[1])
        col3.text(expense[2])
        if col4.button('Delete', key=f'delete_{i}'):
            cursor.execute('DELETE FROM expenses WHERE name = ?', (expense[0],))
            conn.commit()
            st.success('Expense deleted successfully!')






st.set_page_config(page_title="expense", page_icon="📊")
expense()
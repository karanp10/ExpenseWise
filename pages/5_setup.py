import streamlit as st
import sqlite3


conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()


def setup():
    with st.form(key='setup_form'):
        budget = st.number_input('Enter your budget', min_value=0.0)
        categories = st.text_input('Enter your categories (seperated by comma)')

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        categories = [category.strip() for category in categories.split(',')]
        cursor.execute('CREATE TABLE IF NOT EXISTS categories (name TEXT)')
        cursor.execute('CREATE TABLE IF NOT EXISTS budget (amount REAL)')
        cursor.execute('DELETE FROM categories')
        cursor.execute('DELETE FROM budget')        
        for category in categories:
            cursor.execute('INSERT INTO categories VALUES (?)', (category,))
        cursor.execute('INSERT INTO budget VALUES (?)', (budget,))
        conn.commit()
        st.success('Setup completed successfully')
    
    if st.sidebar.button('Delete All Categories'):
        cursor.execute('DELETE FROM categories')
        conn.commit()
        st.success('All categories deleted successfully')

    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()

    
    for category in categories:
        col1, col2 = st.columns([4, 1])
        col1.text(category[0])
        delete_button = col2.button('Delete', key=f'delete_{category[0]}')

        if delete_button:
            cursor.execute('DELETE FROM categories WHERE name = ?', (category[0],))
            conn.commit()
            st.success(f'Category {category[0]} deleted successfully')

st.set_page_config(page_title="Setup", page_icon="📊")
setup()
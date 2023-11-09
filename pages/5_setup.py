import streamlit as st
import sqlite3


conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()


def setup():
    with st.form(key='budget_form'):
        budget = st.number_input('Enter your budget', min_value=0.0)
        submit_budget = st.form_submit_button(label='Submit Budget')

    if submit_budget:
        cursor.execute('DELETE FROM budget')
        cursor.execute('INSERT INTO budget (amount) VALUES (?)', (budget,))
        conn.commit()
        st.success('Budget set successfully')

    with st.form(key='categories_form'):
        categories = st.text_input('Enter your categories (seperated by comma)')
        submit_categories = st.form_submit_button(label='Submit Categories')

    if submit_categories:
        categories = [category.strip() for category in categories.split(',')]
        for category in categories:
            cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (category,))
        conn.commit()
        st.success('Categories set successfully')
    
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
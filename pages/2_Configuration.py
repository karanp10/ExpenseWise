import streamlit as st
import sqlite3
from datetime import datetime


conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys = ON;')


def get_categories(user_id, month):
    cursor.execute('SELECT id, name FROM categories WHERE user_id = ? AND month = ?', (user_id, month))
    return cursor.fetchall()

def setup():

    if 'user_id' not in st.session_state:
        st.write('Please log in to continue')
        st.stop()

    user_id = st.session_state['user_id']

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    current_month = datetime.now().strftime('%B')

    with st.form(key='month_form'):
        month = st.selectbox('Select a month', months, index=months.index(current_month))
        submit_month = st.form_submit_button(label='Select Month')

    

    with st.form(key='budget_form'):
        budget = st.number_input('Enter your budget', min_value=0.0)
        categories_input = st.text_input('Enter your categories (separated by comma)')
        submit_values = st.form_submit_button(label='Submit Budget')

    if submit_values:
        cursor.execute('DELETE FROM budget WHERE user_id = ? AND month = ?', (user_id, month))
        cursor.execute('INSERT INTO budget (user_id, amount, month) VALUES (?, ?, ?)', (user_id, budget, month))
        if len(categories_input) > 1:
            categories_list = [category.strip() for category in categories_input.split(',')]
            for category in categories_list:
                cursor.execute('INSERT INTO categories (user_id, name, month) VALUES (?, ?, ?)', (user_id, category, month))
            conn.commit()
            st.success('Budget set successfully')
        conn.commit()

    # with st.form(key='categories_form'):
    #     categories = st.text_input('Enter your categories (separated by comma)')
    #     submit_categories = st.form_submit_button(label='Submit Categories')

    # if submit_categories:
    #     categories = [category.strip() for category in categories.split(',')]
    #     for category in categories:
    #         cursor.execute('INSERT OR IGNORE INTO categories (user_id, name) VALUES (?, ?)', (user_id, category,))
    #     conn.commit()
    #     st.success('Categories set successfully')
    

    if submit_month:
        # Load the categories for the selected month
        cursor.execute('SELECT id, name FROM categories WHERE user_id = ? AND month = ?', (user_id, month))
        categories = cursor.fetchall()
    
    if st.sidebar.button('Delete All Categories'):
        cursor.execute('DELETE FROM categories WHERE user_id = ? AND month = ?', (user_id, month))
        conn.commit()
        st.success('All categories for ' + month + ' deleted successfully')

    categories = get_categories(user_id, month)

    for i,category in enumerate(categories):

        categories = get_categories(user_id, month)
        col1, col2, col3 = st.columns([4, 1, 1])
        col1.text(category[1]) #display the category name
        delete_button_key = f'delete_{category[0]}'

        if col2.button('Delete', key=delete_button_key):
            cursor.execute('DELETE FROM categories WHERE id = ? AND user_id = ? AND month = ?', (category[0], user_id, month))
            conn.commit()
            st.success(f'Category {category[0]} deleted successfully')
            st.rerun()

        edit_button_key = f'edit_{category[0]}'
        if col3.button('Edit', key=edit_button_key):
            st.session_state.edit = category[0]

        if 'edit' in st.session_state and st.session_state.edit == category[0]:
            with st.form(key=f'edit_form_{category[0]}'):
                new_name = st.text_input('Name', value=category[1])
                submit_button = st.form_submit_button('Update')

                if submit_button:
                    old_name = category[0]
                    cursor.execute('UPDATE expenses SET category = ? WHERE category = ? AND user_id = ? AND month = ?', (new_name, old_name, user_id, month))
                    cursor.execute('UPDATE categories SET name = ? WHERE id = ? AND user_id = ? AND month = ?', (new_name, category[0], user_id, month))
                    conn.commit()
                    st.success('Category updated successfully')
                    del st.session_state.edit
                    st.rerun()
                    
st.set_page_config(page_title="Setup", page_icon="📊")
setup()
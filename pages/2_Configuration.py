import streamlit as st
import sqlite3
from datetime import datetime
from utils import *

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys = ON;')



def setup():

    if 'user_id' not in st.session_state:
        st.write('Please log in to continue')
        st.stop()
    user_id = st.session_state['user_id']
    
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    current_month = datetime.now().strftime('%B')

    #Selecting month
    with st.form(key='month_form'):
        month = st.selectbox('Select a month', months, index=months.index(current_month))
        submit_month = st.form_submit_button(label='Select Month')

    #Entering budget and categories
    with st.form(key='budget_form'):
        budget = st.number_input('Enter your budget', min_value=0.0)
        categories_input = st.text_input('Enter your categories (separated by comma)')
        submit_values = st.form_submit_button(label='Submit Budget')

    #Adding budget and category data
    if submit_values:
        add_budget(conn, cursor, user_id, budget, month)
        add_categories(conn, cursor, user_id, categories_input, month)
    if submit_month:
        categories = fetch_categories(cursor, user_id, month)
    if st.sidebar.button('Delete All Categories'):
        delete_categories(conn, cursor, user_id, month)
        st.success('All categories for ' + month + ' deleted successfully')

    #fetch all categories, including delete and edit functionalities
    categories = fetch_categories(cursor, user_id, month)
    for i,category in enumerate(categories):

        categories = fetch_categories(cursor, user_id, month)
        col1, col2, col3 = st.columns([4, 1, 1])
        col1.text(category[1]) #display the category name
        delete_button_key = f'delete_{category[0]}'

        if col2.button('Delete', key=delete_button_key):
            delete_one_category(conn, cursor, category[0], user_id, month)
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
                    update_category(conn, cursor, new_name, category[0], user_id, month)
                    st.success('Category updated successfully')
                    del st.session_state.edit
                    st.rerun()
                    
st.set_page_config(page_title="Setup", page_icon="📊")
setup()
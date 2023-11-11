import streamlit as st
import sqlite3


conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys = ON;')


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

    cursor.execute('SELECT id,name FROM categories')
    categories = cursor.fetchall()

    
    for i,category in enumerate(categories):
        col1, col2, col3 = st.columns([4, 1, 1])
        col1.text(category[1])
        delete_button_key = f'delete_{category[0]}'

        if col2.button('Delete', key=delete_button_key):
            cursor.execute('DELETE FROM categories WHERE id = ?', (category[0],))
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
                    old_name = category[1]
                    cursor.execute('UPDATE expenses SET category = ? WHERE category = ?', (new_name, old_name))
                    cursor.execute('UPDATE categories SET name = ? WHERE id = ?', (new_name, category[0]))
                    conn.commit()
                    st.success('Category updated successfully')
                    del st.session_state.edit
                    st.rerun()

st.set_page_config(page_title="Setup", page_icon="📊")
setup()
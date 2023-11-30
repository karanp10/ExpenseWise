# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import sqlite3
from auth import check_user, create_user, get_user_id

LOGGER = get_logger(__name__)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()


def run():

    st.set_page_config(
        page_title="Budget Tracker",
        page_icon="👋",
    )

    st.write("# Welcome to ExpenseWise 👋")

    st.write("""
    This Budget Tracker allows you to manage your finances effectively. 
    It includes a budget planner where you can allocate your income to different categories such as necessities, savings, and luxuries based on your preferences. 
    The application also features a dashboard where you can input your expenses for each category and track them. 
    This way, you can have a clear overview of your spending and ensure that it aligns with your budget plan.
    """)

    login_placeholder = st.empty()
    create_placeholder = st.empty()

    if 'user_id' in st.session_state:
        # User is logged in
        st.write("You are logged in!")
        if st.button('Logout'):
            st.session_state.clear()
            st.rerun()
    else:
        # User is not logged in, display the login form
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')

        if login_placeholder.button('Log In', key='login'):
            if check_user(username, password):
                st.session_state['user_id'] = get_user_id(username)
                st.rerun()
            else:
                st.write('Invalid username or password. ')

        if create_placeholder.button('Create Account', key='create_account'):
            success, message = create_user(username, password)
            if success:
                st.session_state['user_id'] = get_user_id(username)
                st.rerun()
            else:
                st.write(message)

if __name__ == "__main__":
    run()

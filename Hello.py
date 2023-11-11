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

LOGGER = get_logger(__name__)

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

def run():

    st.set_page_config(
        page_title="Budget Tracker",
        page_icon="👋",
    )

    st.write("# Welcome to this Budget Tracker 👋")

    st.write("""
    This Budget Tracker allows you to manage your finances effectively. 
    It includes a budget planner where you can allocate your income to different categories such as necessities, savings, and luxuries based on your preferences. 
    The application also features a dashboard where you can input your expenses for each category and track them. 
    This way, you can have a clear overview of your spending and ensure that it aligns with your budget plan.
    """)

if __name__ == "__main__":
    run()

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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
      id INTEGER PRIMARY KEY,
      name TEXT,
      category TEXT,
      amount REAL
    )
               ''')
conn.commit()

def run():

    st.set_page_config(
        page_title="Budget Tracker",
        page_icon="👋",
    )

    st.write("# Welcome to this Budget Tracker 👋")
    manual_budget_input = st.number_input("Budget Amount (Enter manually)", min_value=0.0, value=1000.0)

    expense_name = st.text_input('Expense Name')
    expense_category = st.selectbox("Expense Category", ["Transportation", "Food", "Entertainment"])
    expense_amount = st.number_input('Expense Amount', min_value=0.0)

    if st.button('Add Expense'):

      cursor.execute('INSERT INTO expenses (name, category, amount) VALUES (?, ?, ?)', (expense_name, expense_category, expense_amount)) 
      conn.commit()

      st.success('Expense added successfully!')

    if st.sidebar.button('Delete All Expenses'):
      cursor.execute('DELETE FROM expenses')
      conn.commit()
      st.success('All expenses deleted successfully!')

    if 'delete_id' not in st.session_state:
      st.session_state.delete_id = None
    
    cursor.execute('SELECT id, name, category, amount FROM expenses')
    expenses = cursor.fetchall()

    remaining_budget = manual_budget_input - sum(expense[3] for expense in expenses)

    if remaining_budget >= 0:
      st.success(f'Remaining Budget: ${remaining_budget}')
    else:
      st.error(f'Over budget: ${remaining_budget}')

    st.write('Expenses List')   
    # Display expenses with a delete button
    for expense in expenses:
      st.write(f"ID: {expense[0]}, Name: {expense[1]}, Category: {expense[2]}, Amount: ${expense[3]}")
      delete_button = st.button(f'Delete {expense[0]}', key=f'delete_{expense[0]}')

      if delete_button:
          cursor.execute('DELETE FROM expenses WHERE id = ?', (expense[0],))
          conn.commit()
          st.success(f'Expense {expense[0]} deleted successfully!')
          expenses = [e for e in expenses if e[0] != expense[0]]



if __name__ == "__main__":
    run()

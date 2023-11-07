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

LOGGER = get_logger(__name__)


def run():
    expenses  = []

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

      expense = {
        'name': expense_name,
        'category': expense_category,
        'amount': expense_amount
      }

      expenses.append(expense)

      st.success('Expense added successfully!')
    
    remaining_budget = manual_budget_input - sum(expense['amount'] for expense in expenses)

    if remaining_budget >= 0:
      st.success(f'Remaining Budget: ${remaining_budget}')
    else:
      st.error(f'Over budget: ${remaining_budget}')

    st.write('Expenses List')
    for expense in expenses:
      st.write(f"Name: {expense['name']}, Category: {expense['category']}, Amount: ${expense['amount']}")


    st.sidebar.success("Select a demo above.")



if __name__ == "__main__":
    run()

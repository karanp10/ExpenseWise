import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
from utils import *

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def budget_planner():
    st.title('Budget Planner')

    if 'user_id' not in st.session_state:
        st.write('Please log in to continue')
        st.stop()

    user_id = st.session_state['user_id']
    col1, col2 = st.columns(2)

    #Input for Income
    income = col1.number_input('Enter your income', min_value = 0.0)
    if col1.button('Submit Income'):
        add_income(conn, cursor, user_id, income)

    #Mandatory Expense
    col1.subheader('Mandatory Expenses')
    categories = [row[0] for row in fetch_group_name(cursor)]
    category_name = col1.selectbox('Select a category', categories)
    expense_name = col1.text_input('Enter the name of the expense')
    amount = col1.number_input('Enter the amount', min_value = 0.0)
    if col1.button('Submit Expense'):
        category_id = fetch_group_id(cursor, category_name)
        add_mandatory_expenses(conn, cursor, user_id, category_id, expense_name, amount)

    #Latest Income
    latest_income = fetch_latest_income(cursor, user_id)
    if latest_income:
        # Display the income in col2 as a subheader
        col2.subheader(f"Income: {latest_income[0]}")

    #Get Mandatory Expenses and Display
    expenses = fetch_mandatory_expenses(cursor, user_id)
    if expenses:
        df = pd.DataFrame(expenses, columns=['ID', 'Category', 'Expense', 'Amount'])
        df['Amount'] = df['Amount'].round(2).astype(str)
        
        with col2:
            for index, row in df.iterrows():
                cols = st.columns([3,3,3,1])
                cols[0].markdown(f"{row['Category']}")
                cols[1].markdown(f"{row['Expense']}")
                cols[2].markdown(f"{row['Amount']}")
                if cols[3].button(label=':x:', key=row['ID']):
                    delete_mandatory_expense(conn, cursor, row['ID'], user_id)
                    st.rerun()

    
    #Tolerance sliders
    col1.subheader('Set Tolerance')
    necessities = col1.slider('Necessities', min_value = 0, max_value = 100, value = 50)
    savings = col1.slider('Savings', min_value = 0, max_value = 100, value = 30)
    luxuries = col1.slider('Luxuries', min_value = 0, max_value = 100, value = 20)


    #Calculation for each category
    latest_income = fetch_latest_income(cursor, user_id)
    if latest_income:
        col2.subheader("Allocation Before Expenses")
        
        if necessities + savings + luxuries == 100:
            necessities_budget = latest_income[0] * necessities / 100
            savings_budget = latest_income[0] * savings / 100
            luxuries_budget = latest_income[0] * luxuries / 100

            col2.text(f"Necessities:{necessities_budget}")
            col2.text(f"Savings: {savings_budget}")
            col2.text(f"Luxuries: {luxuries_budget}")

            category_ids = fetch_distinct_group_id(cursor, user_id)
            category_names = {id: name for id, name in fetch_group_info(cursor)}
            category_expenses = {}

            for category_id in category_ids:
                category_id = category_id[0]
                total_expenses = fetch_total_expenses(cursor, category_id, user_id)
                category_expenses[category_names[category_id]] = total_expenses

            necessities_expenses = category_expenses.get('Necessities', 0)
            savings_expenses = category_expenses.get('Savings', 0)
            luxuries_expenses = category_expenses.get('Luxuries', 0)
                        
            necessities_left = necessities_budget - necessities_expenses
            savings_left = savings_budget - savings_expenses
            luxuries_left = luxuries_budget - luxuries_expenses

            col2.subheader("Allocation After Expenses")

            col2.text(f"Necessities left: {necessities_left}")
            col2.text(f"Savings left: {savings_left}")
            col2.text(f"Luxuries left: {luxuries_left}")
        else:
            col2.warning('The sum of the 3 categories must equal 100')



st.set_page_config(page_title='budget_automater')
budget_planner()
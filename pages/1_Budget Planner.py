import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

conn = sqlite3.connect('budget.db')
cursor = conn.cursor()

def budget_planner():
    st.title('Budget Planner')

    col1, col2 = st.columns(2)

    #Input for Income
    income = col1.number_input('Enter your income', min_value = 0.0)
    if col1.button('Submit Income'):
        cursor.execute('INSERT INTO income (amount) VALUES (?)', (income,))
        conn.commit()

    col1.subheader('Mandatory Expenses')
    categories = [row[0] for row in cursor.execute('SELECT name FROM categories')]
    category_name = col1.selectbox('Select a category', categories)
    expense_name = col1.text_input('Enter the name of the expense')
    amount = col1.number_input('Enter the amount', min_value = 0.0)
    if col1.button('Submit Expense'):
        cursor.execute('Select id FROM categories WHERE name = ?', (category_name,))
        category_id = cursor.fetchone()[0]
        cursor.execute('INSERT INTO mandatory_expenses (category_id, name, amount) VALUES (?, ?, ?)', (category_id, expense_name, amount))
        conn.commit()

    latest_income = cursor.execute('SELECT amount FROM income ORDER BY rowid DESC LIMIT 1').fetchone()

    if latest_income:
        # Display the income in col2 as a subheader
        col2.subheader(f"Income: {latest_income[0]}")

    expenses = cursor.execute('SELECT mandatory_expenses.id, categories.name, mandatory_expenses.name, mandatory_expenses.amount FROM mandatory_expenses JOIN categories ON mandatory_expenses.category_id = categories.id').fetchall()

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
                    cursor.execute('DELETE FROM mandatory_expenses WHERE id = ?', (row['ID'],))
                    conn.commit()
                    st.rerun()

    col1.subheader('Set Tolerance')
    necessities = col1.slider('Necessities', min_value = 0, max_value = 100, value = 50)
    savings = col1.slider('Savings', min_value = 0, max_value = 100, value = 30)
    luxuries = col1.slider('Luxuries', min_value = 0, max_value = 100, value = 20)


    latest_income = cursor.execute('SELECT amount FROM income ORDER BY rowid DESC LIMIT 1').fetchone()

    if latest_income:
        col2.subheader("Allocation Before Expenses")
        
        if necessities + savings + luxuries == 100:
        # Calculate the budget for each category
            necessities_budget = latest_income[0] * necessities / 100
            savings_budget = latest_income[0] * savings / 100
            luxuries_budget = latest_income[0] * luxuries / 100

            col2.text(f"Necessities: {necessities_budget}")
            col2.text(f"Savings: {savings_budget}")
            col2.text(f"Luxuries: {luxuries_budget}")

            category_ids = cursor.execute('SELECT DISTINCT category_id FROM mandatory_expenses').fetchall()
            category_names = {id: name for id, name in cursor.execute('SELECT id, name FROM categories').fetchall()}
            category_expenses = {}

            for category_id in category_ids:
                category_id = category_id[0]
                total_expenses = cursor.execute('SELECT SUM(amount) FROM mandatory_expenses WHERE category_id = ?', (category_id,)).fetchone()[0] or 0
                category_expenses[category_names[category_id]] = total_expenses

            # Now you can access the expenses for each category using the category names
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
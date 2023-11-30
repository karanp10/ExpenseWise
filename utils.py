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

import inspect
import textwrap
import sqlite3
import calendar
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import streamlit as st


conn = sqlite3.connect('database.db')

def fetch_group_id(cursor, category_name):
    cursor.execute('SELECT id FROM groups WHERE name = ?', (category_name,))
    return cursor.fetchone()[0]

def fetch_group_name(cursor):
    names = cursor.execute('SELECT name FROM groups')
    return names 

def fetch_distinct_group_id(cursor, user_id):
    category_ids = cursor.execute('SELECT DISTINCT group_id FROM mandatory_expenses WHERE user_id = ?', (user_id,)).fetchall()
    return category_ids

def fetch_group_info(cursor):
    group_info = cursor.execute('SELECT id, name FROM groups').fetchall()
    return group_info


def fetch_total_expenses(cursor, category_id, user_id):
    expenses = cursor.execute('SELECT SUM(amount) FROM mandatory_expenses WHERE group_id = ? AND user_id = ?', (category_id, user_id)).fetchone()[0] or 0
    return expenses
    

def fetch_categories_names(cursor, user_id, month):
    cursor.execute('SELECT name FROM categories WHERE user_id = ? AND month = ?', (user_id, month))
    categories = [category[0] for category in cursor.fetchall()]
    return categories

def fetch_latest_income(cursor, user_id):
    latest_income = cursor.execute('SELECT amount FROM income WHERE user_id = ? AND amount IS NOT NULL ORDER BY rowid DESC LIMIT 1', (user_id,)).fetchone()
    return latest_income

def fetch_mandatory_expenses(cursor, user_id):
    expenses = cursor.execute('SELECT mandatory_expenses.id, groups.name, mandatory_expenses.name, mandatory_expenses.amount FROM mandatory_expenses JOIN groups ON mandatory_expenses.group_id = groups.id WHERE mandatory_expenses.user_id = ? AND mandatory_expenses.amount IS NOT NULL', (user_id,)).fetchall()
    return expenses

def fetch_categories(cursor, user_id, month):
    cursor.execute('SELECT id, name FROM categories WHERE user_id = ? AND month = ?', (user_id, month))
    return cursor.fetchall()

def fetch_category_id(cursor, user_id, month, category_name):
    cursor.execute('SELECT id FROM categories WHERE name = ? AND user_id = ? AND month = ?', (category_name, user_id, month))
    return cursor.fetchone()[0]

def fetch_budget(cursor, user_id, month):
    cursor.execute('SELECT amount FROM budget WHERE user_id = ? AND month = ?', (user_id, month))
    budget = cursor.fetchone()
    return budget[0] if budget is not None else 0

def fetch_expenses(cursor, user_id, month):
    cursor.execute('SELECT e.id, e.name, c.name, e.amount, e.date FROM expenses e INNER JOIN categories c ON e.category_id = c.id WHERE e.user_id = ? AND e.month = ?', (user_id, month))
    return cursor.fetchall()

def fetch_sum_expenses(cursor, user_id, month):
    cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ? AND month = ?', (user_id, month))
    expenses = cursor.fetchone()[0]
    return expenses if expenses is not None else 0

def add_income(conn, cursor, user_id, income):
    cursor.execute('INSERT INTO income (user_id, amount) VALUES (?, ?)', (user_id, income))
    conn.commit()

def add_mandatory_expenses(conn, cursor, user_id, group_id, expense_name, amount):
    cursor.execute('INSERT INTO mandatory_expenses (user_id, group_id, name, amount) VALUES (?, ?, ?, ?)', (user_id, group_id, expense_name, amount))
    conn.commit()

def add_expense(conn, cursor, user_id, name, category, amount, month):
    cursor.execute('SELECT id FROM categories WHERE name = ? AND user_id = ? AND month = ?', (category, user_id, month))
    category_id = cursor.fetchone()[0]
    date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('INSERT INTO expenses (user_id, name, category_id, amount, date, month) VALUES (?, ?, ?, ?, ?, ?)', (user_id, name, category_id, amount, date, month))
    conn.commit()

def add_budget(conn, cursor, user_id, budget, month):
    cursor.execute('DELETE FROM budget WHERE user_id = ? AND month = ?', (user_id, month))
    cursor.execute('INSERT INTO budget (user_id, amount, month) VALUES (?, ?, ?)', (user_id, budget, month))
    conn.commit()

def add_categories(conn, cursor, user_id, categories_input, month):
    if len(categories_input) > 1:
        categories_list = [category.strip() for category in categories_input.split(',')]
        for category in categories_list:
            cursor.execute('INSERT INTO categories (user_id, name, month) VALUES (?, ?, ?)', (user_id, category, month))
        conn.commit()
        st.success('Budget set successfully')

def delete_mandatory_expense(conn, cursor, id, user_id):
    cursor.execute('DELETE FROM mandatory_expenses WHERE id = ? AND user_id = ?', (id, user_id))
    conn.commit()

def delete_expense(conn, cursor, id, user_id):
    cursor.execute('DELETE FROM expenses WHERE id = ? AND user_id = ?', (id, user_id))
    conn.commit()

def delete_month_expense(conn, cursor, user_id, month):
    cursor.execute('DELETE FROM expenses WHERE user_id = ? AND month = ?', (user_id, month))
    conn.commit()

def delete_categories(conn, cursor, user_id, month):
    cursor.execute('DELETE FROM categories WHERE user_id = ? AND month = ?', (user_id, month))
    conn.commit()

def delete_one_category(conn, cursor, category_id, user_id, month):
    cursor.execute('DELETE FROM categories WHERE id = ? AND user_id = ? AND month = ?', (category_id, user_id, month))
    conn.commit()

def update_expense(conn, cursor, new_name, new_category_id, new_amount, new_date, expense_id, user_id):
    cursor.execute('UPDATE expenses SET name = ?, category_id = ?, amount = ?, date = ? WHERE id = ? AND user_id = ?', (new_name, new_category_id, new_amount, new_date.strftime('%Y-%m-%d'), expense_id, user_id))
    conn.commit()

def update_category(conn, cursor, new_name, category_id, user_id, month):
    cursor.execute('UPDATE categories SET name = ? WHERE id = ? AND user_id = ? AND month = ?', (new_name, category_id, user_id, month))
    conn.commit()

def category_chart(cursor, user_id, month, col1):
    cursor.execute('SELECT c.name, SUM(e.amount) FROM expenses e INNER JOIN categories c ON category_id = c.id WHERE e.user_id = ? AND e.month = ? GROUP BY c.name', (user_id, month))
    #cursor.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id = ? AND month = ? GROUP BY category', (user_id, month))
    category_expenses = cursor.fetchall()

    categories = [row[0] for row in category_expenses]
    amounts = [row[1] for row in category_expenses]

    by_category = col1.selectbox('By Category', ['Pie Chart', 'Bar Chart'])

    color_dict = {category: color for category, color in zip(categories, px.colors.qualitative.Plotly)}

    if by_category == 'Pie Chart':
        fig = go.Figure(data=[go.Pie(labels=categories, values=amounts, hole=.3, marker_colors=[color_dict[category] for category in categories])])
        fig.update_layout(autosize=False, width=350, height=500)
        col1.plotly_chart(fig)
    elif by_category == 'Bar Chart':
        fig = go.Figure(data=[go.Bar(x=categories, y=amounts, marker_color=[color_dict[category] for category in categories])])
        fig.update_layout(autosize=False, width=350, height=500)
        col1.plotly_chart(fig)

def expense_category_chart(cursor, user_id, month, col2):
    cursor.execute('SELECT c.name, SUM(e.amount) FROM expenses e INNER JOIN categories c ON e.category_id = c.id WHERE e.user_id = ? AND e.month = ? GROUP BY c.name', (user_id, month))
    #cursor.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id = ? AND month = ? GROUP BY category', (user_id, month))
    category_expenses = cursor.fetchall()
    categories = [row[0] for row in category_expenses]

    category_to_view = col2.selectbox('Select a category to view', categories)
    cursor.execute('SELECT e.name, SUM(e.amount) FROM expenses e INNER JOIN categories c ON e.category_id = c.id WHERE c.name = ? AND e.user_id = ? AND e.month = ? GROUP BY e.name', (category_to_view, user_id, month))
    #cursor.execute('SELECT name, SUM(amount) FROM expenses WHERE category = ? AND user_id = ? AND month = ? GROUP BY name',  (category_to_view, user_id, month))
    individual_expenses = cursor.fetchall()

    expense_names = [row[0] for row in individual_expenses]
    amounts = [row[1] for row in individual_expenses]

    fig = go.Figure(data=[go.Pie(labels=expense_names, values=amounts, hole=.3)])
    fig.update_layout(autosize=False, width=350, height=500)
    col2.plotly_chart(fig)

def track_spending_chart(cursor, user_id, month, budget):
    current_date = datetime.now().date()  
    current_year = datetime.now().year
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_index = months.index(month) + 1

    #calculate number of days in current month
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]

    #calculate daily budget
    daily_budget = budget / days_in_month
    start_date = f"{current_year}-{month_index:02d}-01"
    end_date = f"{current_year}-{month_index:02d}-{calendar.monthrange(current_year, month_index)[1]}"

      # Create a DataFrame with dates of the month
    df = pd.DataFrame({
        'date': pd.date_range(start=start_date, end=end_date)
    })

    # Calculate the expected spending for each day
    df['expected_spending'] = daily_budget * (df['date'].dt.day)

    # Fetch the daily spending up to the current date
    cursor.execute('SELECT date, SUM(amount) FROM expenses WHERE user_id = ? AND date >= ? AND date <= ? GROUP BY date', (user_id, start_date, current_date))
    daily_spending = cursor.fetchall()

    # Convert the daily spending into a DataFrame
    df_spending = pd.DataFrame(daily_spending, columns=['date', 'amount'])
    df_spending['date'] = pd.to_datetime(df_spending['date'])

    # Merge the two DataFrames
    df = pd.merge(df, df_spending, how='left', on='date')

    # Calculate the cumulative spending
    df['amount'] = df['amount'].fillna(0)
    df['current_spending'] = df['amount'].cumsum()
    current_date = pd.to_datetime(current_date)
    df.loc[df['date'] > current_date, 'current_spending'] = np.nan


    # Create a line chart with two lines
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['current_spending'], mode='lines', name='Current Spending'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['expected_spending'], mode='lines', name='Expected Spending'))
    fig.update_layout(title='Spending Over Time', xaxis_title='Date', yaxis_title='Amount')

    # Set the range of the x-axis
    fig.update_xaxes(range=[start_date, end_date])

    # Display the chart
    return fig

def treemap_expense(cursor, user_id, month):
    cursor.execute('SELECT name, SUM(amount) as total_amount FROM expenses WHERE user_id = ? AND month = ? GROUP BY name ORDER BY total_amount DESC LIMIT 10', (user_id, month))
    top_expenses = cursor.fetchall()
    df = pd.DataFrame(top_expenses, columns = ['Expense', 'Amount'])
    df['Label'] = df['Expense'] + '<br>$' + df['Amount'].astype(str)
    fig = px.treemap(df, path=['Label'], values='Amount', title='Top Expenses This Month', hover_data=['Expense'])
    fig.data[0].hovertemplate = '%{label}%'
    return fig



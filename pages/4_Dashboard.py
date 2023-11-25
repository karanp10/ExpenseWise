import streamlit as st
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import numpy as np
import pandas as pd
from utils import *


conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def budget():

    if 'user_id' not in st.session_state:
        st.write('Please log in to continue')
        st.stop()
    user_id = st.session_state['user_id']

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    current_month = datetime.now().strftime('%B')
    with st.form(key='month_form'):
        month = st.selectbox('Select a month', months, index=months.index(current_month))
        submit_month = st.form_submit_button(label='Select Month')

    if submit_month:
        x = 0
        
        # Load the budget for the selected month

    budget = fetch_budget(cursor, user_id, month)
    expenses = fetch_sum_expenses(cursor, user_id, month)
    remaining_amount = budget - expenses

    
    col1, col2 = st.columns([1,1])
    col1.metric(label='Budget', value=f'${budget}')
    col2.metric(label='Remaining', value=f"${remaining_amount}", delta=f"-${expenses}")

    #budget vs spending per day
    fig = track_spending_chart(cursor, user_id, month, budget)
    st.plotly_chart(fig)

    chart_col1, chart_col2 = st.columns([1,1])
    #category by category expense list
    category_chart(cursor, user_id, month, chart_col1)

    #expense per category list
    expense_category_chart(cursor, user_id, month, chart_col2)

    # cursor.execute('SELECT date, SUM(amount) FROM expenses WHERE user_id = ? AND month = ? AND strftime("%m", date) = strftime("%m", "now") GROUP BY date', (user_id, month))
    # expenses_by_date = cursor.fetchall()

    # dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in expenses_by_date]
    # amounts = [row[1] for row in expenses_by_date] 

    # fig = go.Figure(data=go.Scatter(x=dates, y=amounts))
    # fig.update_layout(title='Expenses Over Time', xaxis_title = 'Date', yaxis_title = 'Amount')  
    # fig.update_xaxes(range=[start_date, end_date])
               
    # st.plotly_chart(fig) 



    

st.set_page_config(page_title="budget", page_icon="📊")
budget()

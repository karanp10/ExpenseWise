import streamlit as st
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import numpy as np
import pandas as pd
from utils import *
import plotly.figure_factory as ff

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def budget():

    if 'user_id' not in st.session_state:
        st.write('Please log in to continue')
        st.stop()
    user_id = st.session_state['user_id']

    #Selecting Month 
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    current_month = datetime.now().strftime('%B')
    with st.form(key='month_form'):
        month = st.selectbox('Select a month', months, index=months.index(current_month))
        submit_month = st.form_submit_button(label='Select Month')
    if submit_month:
        x = 0 #placeholder

    # Load the budget, expenses for the selected month
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

    #treemap of expenses
    fig = treemap_expense(cursor, user_id, month)
    st.plotly_chart(fig)

            


    

st.set_page_config(page_title="budget", page_icon="📊")
budget()

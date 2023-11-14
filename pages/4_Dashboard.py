import streamlit as st
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def budget():

    if 'user_id' not in st.session_state:
        st.write('Please log in to continue')
        st.stop()
    user_id = st.session_state['user_id']


    cursor.execute('SELECT amount FROM budget WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    budget = result[0] if result is not None else 0

    cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ?', (user_id,))
    expenses = cursor.fetchone()[0]
    if expenses is None:
        expenses = 0
    
    remaining = budget - expenses
    col1, col2 = st.columns([1,1])
    col1.metric(label='Budget', value=f'${budget}')
    col2.metric(label='Remaining', value=f"${remaining}", delta=f"-${expenses}")

    cursor.execute('SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category', (user_id,))
    category_expenses = cursor.fetchall()

    categories = [row[0] for row in category_expenses]
    amounts = [row[1] for row in category_expenses]

    by_category = st.selectbox('By Category', ['Pie Chart', 'Bar Chart'])

    color_dict = {category: color for category, color in zip(categories, px.colors.qualitative.Plotly)}

    if by_category == 'Pie Chart':
        fig = go.Figure(data=[go.Pie(labels=categories, values=amounts, hole=.3, marker_colors=[color_dict[category] for category in categories])])
        fig.update_layout(autosize=False, width=800, height=700)
        st.plotly_chart(fig)
    elif by_category == 'Bar Chart':
        fig = go.Figure(data=[go.Bar(x=categories, y=amounts, marker_color=[color_dict[category] for category in categories])])
        fig.update_layout(autosize=False, width=800, height=700)
        st.plotly_chart(fig)

    category_to_view = st.selectbox('Select a category to view', categories)
    cursor.execute('SELECT name, SUM(amount) FROM expenses WHERE category = ? AND user_id = ? GROUP BY name',  (category_to_view, user_id))
    individual_expenses = cursor.fetchall()

    expense_names = [row[0] for row in individual_expenses]
    amounts = [row[1] for row in individual_expenses]

    fig = go.Figure(data=[go.Pie(labels=expense_names, values=amounts, hole=.3)])
    fig.update_layout(autosize=False, width=800, height=700)
    st.plotly_chart(fig)



    

st.set_page_config(page_title="budget", page_icon="📊")
budget()

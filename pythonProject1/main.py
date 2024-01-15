import streamlit as st
import requests
import yfinance as yf
import pandas as pd
import plotly.express as px
import time
import datetime
from streamlit_extras.switch_page_button import switch_page
import random
import json
import os

check = False

data = []
a = False


st.set_page_config(
    page_title="Stocks analyzer",
    page_icon=r"icons8-stock-48.png",

)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False


def click_button():
    st.session_state.clicked = True



json_file_path = "users.json"


def stockanalyzer():
    st.title("Stock Analyzer")
    company_name = st.text_input("Enter company name or item:")

    min_date = datetime.date(2022, 1, 1)
    max_date = datetime.datetime.now() - datetime.timedelta(days=16)
    start_date = st.date_input("Select start date:",
                               min_value=min_date,
                               max_value=max_date,
                               value=min_date)

    end_date = datetime.datetime.now().date()

    st.button('Analyze', on_click=click_button)
    if st.session_state.clicked:
        if company_name == "":
            st.warning("You have to enter a stock or a company name.")
        else:
            if company_name.upper() == "APPLE" or company_name.upper() == "AAPL" or company_name.upper() == "APLE":
                stock_symbol = "AAPL"
            elif company_name.upper() == "NVDA" or company_name.upper() == "NVIDIA" or company_name.upper() == "NVIDA":
                stock_symbol = "NVDA"
            else:
                with st.spinner("Fetching stock symbol..."):
                    stock_symbol = get_stock_symbol(company_name)
            if stock_symbol:
                st.title("Stock Price Visualization App")
                st.write(f"Displaying stock data for {stock_symbol}")

                with st.spinner("Fetching stock data..."):
                    stock_data = get_stock_data(stock_symbol, start_date, end_date)

                if stock_data is not None:
                    plot_stock_data(stock_data)
                    lowest_point = stock_data['Close'].min()
                    highest_point = stock_data['Close'].max()
                    chart_data = pd.DataFrame({
                        'Date': stock_data.index,
                        'Stock Price': stock_data['Close'],
                        'Lowest Point': lowest_point,
                        'Highest Point': highest_point
                    })
                    st.line_chart(chart_data.set_index('Date'))
                    st.success(f"Highest Stock Price: ${round(highest_point, 2)}")
                    st.warning(f"Lowest Stock Price: ${round(lowest_point, 2)}")
                    try:
                        with st.spinner("Performing predictions..."):
                            predicted_value_lr = predict_tomorrows_stock_value_linear_regression(stock_data)
                            predicted_value_lstm = predict_tomorrows_stock_value_lstm(stock_data)
                            time.sleep(1)

                        st.write(f"Approximate tomorrow's stock value (Linear Regression): {predicted_value_lr:.2f}$")
                        st.write(f"Approximate tomorrow's stock value (LSTM): {predicted_value_lstm:.2f}$")

                        with st.expander("💡 What is LSTM?"):
                            display_lstm_info()

                        with st.expander("💡 What is Linear Regression?"):
                            st.write("Linear Regression Simulation:")
                            linear_Regression(stock_data)



                    except:
                        st.warning("Not enough info for an AI approximation, please try an earlier date.")
            else:
                st.warning(f"Stock doesn't exist.\ntry again or check your input.")

def user_exists(username):
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            file_contents = file.read()
            if file_contents:
                try:
                    users = json.loads(file_contents)
                except json.JSONDecodeError:
                    st.error("Error decoding JSON. Please check the file format.")
                    return False
            else:
                users = {}
                with open(json_file_path, "w") as empty_file:
                    json.dump(users, empty_file)
    else:
        users = {}
    return username in users


def sign_up(username, password, fav_team):
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            file_contents = file.read()
            if file_contents:
                try:
                    users = json.loads(file_contents)
                except json.JSONDecodeError:
                    st.error("Error decoding JSON. Please check the file format.")
                    return
            else:
                users = {}
    else:
        users = {}

    if username in users:
        st.warning("Username is already taken. Please choose another one.")
    else:
        user_data = {"password": password, "fav_team": fav_team}
        users[username] = user_data
        with open(json_file_path, "w") as file:
            json.dump(users, file)
        st.success("You have successfully signed up!")




# Function to sign in a user
def Login(username, password):
    if user_exists(username):
        with open(json_file_path, "r") as file:
            users = json.load(file)
            user_data = users.get(username)
            if user_data and user_data.get("password") == password:
                fav_team = user_data.get("fav_team")
                if fav_team:
                    st.success(f"Welcome, {username}! favorite team: {fav_team}")
                else:
                    fav_team = "None"
                    st.success(f"Welcome, {username}!")
            else:
                st.warning("Incorrect password. Please check for spelling and try again.")
    else:
        st.warning("User does not exist. Please sign up or check the username.")

def Account():
    st.title("hi")

def homepage():
    st.title("BasketBall - Team Information")
    want = st.button("hi")
    if want:
        switch_page("Login")
    page = st.sidebar.radio("Navigation", ["Sign Up", "Login"])

    if page == "Sign Up":
        st.header("Sign Up")
        username = st.text_input("Enter your username:")
        password = st.text_input("Enter your password:", type="password")
        fav_team = st.text_input("Enter your favorite team (optional):")
        if st.button("Sign Up"):
            sign_up(username, password, fav_team)
            return username,password,fav_team

    elif page == "Login":
        st.header("Login")
        username = st.text_input("Enter your username:")
        password = st.text_input("Enter your password:", type="password")
        if st.button("Login"):
            if Login(username, password):
                with open(json_file_path, "r") as file:
                    users = json.load(file)
                    user_data = users.get(username)
                    fav_team = user_data.get("fav_team")
                return username, password, fav_team
            if username and password:
                st.sidebar.radio("Select Page", ["Information", "real time stock investment"])



page = st.sidebar.radio("Select Page", ["Home", "Information", "real time stock investment"])
if page == "Home":
    homepage()
elif page == "Information":
    pass
elif page == "real time stock investment":
    pass

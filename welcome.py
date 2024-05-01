import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm
import streamlit as st
import plotly.express as px

# -------- H E A D E R -------- #
st.title("Risk Analysis of Stocks")

# -------- F O R M -------- #
with st.form("my_form", clear_on_submit=True):

    st.write("Enter the Stock or Index Ticker:")
    tickers = st.text_input("(separated by comma ' , ' without giving space): ")

    st.write("Enter the start date:")
    start_date = st.text_input("(YYYY-MM-DD):")

    st.write("Enter the end date:")
    end_date = st.text_input("(YYYY-MM-DD): ")

    submitted = st.form_submit_button('Submit')

# --------- A F T E R - S U B M I S S I O N -------- #
if submitted:
    st.subheader("Selected Data")
    c1,c2 = st.columns(2)
    with c1:
        st.write("Selected Ticker/s: ")
        st.write("Start Date: ")
        st.write("End Date: ")
    with c2:
        st.write("INFY.NS, TCS.NS, TECHM.NS, WIPRO.NS")
        st.write("2014-01-01")
        st.write("2024-01-01")
    
    # -------- D A T A - D O W N L O A D -------- #
    stock_raw = yf.download(["INFY.NS","TCS.NS","TECHM.NS","WIPRO.NS"], start='2014-01-01', end='2024-01-01')
    stock_data = pd.DataFrame(stock_raw)
    stock_data = stock_data.loc[:,'Close']

    # -------- D A T A - P R E V I E W -------- #
    st.subheader("Data Preview (Only Closing Price)")
    st.dataframe(stock_data, use_container_width=True)

    # -------- C O M P A R I S O N - C H A R T -------- #
    st.subheader("Stock Comparison Chart")
    fig = px.line(stock_data)
    st.plotly_chart(fig)

    # -------- C A L C U L A T I O N -------- #
    data = stock_data.pct_change().dropna()
    agg_data = data.describe().T.loc[:,["mean","std"]]
    agg_data["mean"] = agg_data["mean"] * 251
    agg_data["std"] = agg_data["std"] * np.sqrt(251)

    # -------- R I S K - C O M P A R I S O N ------- #
    st.subheader("Risk Comparison Chart")
    fig1 = px.scatter(agg_data, x="std", y="mean", color=agg_data.index, symbol=agg_data.index)
    st.plotly_chart(fig1)

    # -------- VALUE AT RISK (Monte Carlo) -------- #
    
    
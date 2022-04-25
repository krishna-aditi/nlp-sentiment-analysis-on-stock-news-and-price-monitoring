# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 22:31:39 2022

@author: krish
"""

import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import yfinance as yf
import requests

def price_plot(data_frame, comp):
    fig = px.line(data_frame, x="Date", y="High", labels={"Date": "Date",  "High": "High Price of Stock"}, width=750, height=500, template="plotly_dark")
    html_temp = f"""
        <div style="background-color:PowderBlue;padding:2px">
        <h2 style="color:Black;text-align:center;">Stock price monitor for {comp}</h2>
        </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    st.plotly_chart(fig)

def comp_fin(info_summary_df, comp):
    html_temp = f"""
        <div style="background-color:PowderBlue;padding:2px">
        <h2 style="color:Black;text-align:center;">{comp} Quarterly Financials</h2>
        </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(info_summary_df)

def comp_summary(info, comp):
    html_temp = f"""
        <div style="background-color:PowderBlue;padding:2px">
        <h2 style="color:Black;text-align:center;">About {comp}</h2>
        </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    html_temp2 = f"""
        <div>
        <body style="color:white;align:"justify";">{info}</body>
        </div>
    """   
    st.markdown(html_temp2, unsafe_allow_html=True)

def comp_news(news, comp):
    html_temp = f"""
        <div style="background-color:PowderBlue;padding:2px">
        <h2 style="color:Black;text-align:center;">{comp} News</h2>
        </div>
    """
    st.markdown("")
    st.markdown(html_temp, unsafe_allow_html=True)
    html_temp2 = f' <div> <body style="color:white;align:"justify";">'  
    
    for n in news:
        html_temp2 += f"<h2>{n['title']}</h2><p>{n['content']}</p> \n"
        
    html_temp2 += "</body>  </div>"   
    st.markdown(html_temp2, unsafe_allow_html=True)
def main():
    html_temp_title = f"""
        <div style="background-color:SteelBlue;padding:4px">
        <h1 style="color:white;text-align:center;">NLP and Sentiment Analysis on Stock Market News with Price Monitoring Dashboard</h1>
        </div>
    """
    st.markdown(html_temp_title, unsafe_allow_html=True)
        
    page = st.sidebar.radio("Navigation Pane", ["Login page", "About the company", "Company news", "API Live Dashboard"])
    s = st.session_state
    if page == "Login page":
        username = st.text_input("User Name: ")
        password = st.text_input("Password: ", type="password")
            
        authjson = { "username": f"{username}", "password": f"{password}"}
        headers = {"Authorization": f"Basic Og=="}
        
        if not s:
            s.token = ''
            s.authenticated = False
            s.company = ''
        col1, col2 = st.columns([0.2,1])
        if col1.button("Login")  or s.authenticated:
            
            if (username and password) or s.authenticated:
                s.authenticated = True
                token = requests.post("http://127.0.0.1:8000/token", data = authjson)
                if col2.button("Log Out"):
                    s.authenticated = False
                    token = None
                    s.token = ''
                    s.company = ''
                    st.markdown(f"Log Out Successful!")
                    return None
                                
                if token.status_code == 200: 
                     s.authenticated = True
                     s.token = token.json()['access_token']
                     st.markdown(f"Login Successful! You now have access to explore other pages!")
                
            else:
                st.markdown('Please Enter Valid Username and Password')
                    
    if page == "About the company":
        if not s.authenticated:
            st.markdown(f"Please Login to Access this Page.")
        else:
            st.subheader("Choose company:")
            comp_name = st.selectbox("",("AAPL-Apple", "MSFT-Microsoft", "AMZN-Amazon", "WMT-Walmart", "GOOG-Alphabet", "FB-Meta", "TSLA-Tesla", "NVDA-NVIDIA", "PFE-Pfizer", "NFLX-Netflix"))
            s.company = ''
            comp = comp_name.split("-")[0].strip()
            params_test = {"company_name": comp}
            if st.button("Fetch"):
                s.company = comp_name.split('-')[-1].strip()
                headers = {"Authorization": f"Bearer {s.token}"}
                info_test = requests.post("http://127.0.0.1:8000/stocks/stock_info", headers=headers, json = params_test)   
                if info_test.status_code == 200:
                    output = info_test.json()
                    # Lineplot for High column
                    if 'Error' in output.keys():
                        st.markdown(f"{output['Error']}")
                    else:
                        st.markdown("")
                        comp_summary(output['Info'], comp_name)
                        st.markdown("")
                        price_plot(output['Price'], comp_name)
                        st.markdown("")
                        comp_fin(output['Finance'], comp_name)
                        st.markdown("")
    if page == "Company news":
        headers = {"Authorization": f"Bearer {s.token}"}
        if s.company != '':
            params_test = {"company_name": s.company}
            response = requests.post("http://127.0.0.1:8000/stocks/news", headers=headers, json = params_test)
            if response.status_code == 200:
                output = response.json()
                # Lineplot for High column
                if 'Error' in output.keys():
                    st.markdown(f"{output['Error']}")
                else:
                    comp_news(output['News'], s.company)
                    
        else:
            st.markdown("Please Select a Company and Fetch details in 'About Company' Page!!") 
    if page == "API Live Dashboard":
        headers = {"Authorization": f"Bearer {s.token}"}
        response = requests.post("http://127.0.0.1:8000/stocks/dashboard", headers=headers)
        if response.status_code == 200:
            url = response.json()['url']
            st.markdown(f"""
                        <iframe width="700" height="550" src={url} frameborder="0" style="border:0" allowfullscreen></iframe>
                        """, unsafe_allow_html=True)
        else:
            st.markdown(f"Not an Admin! Stocks API Dashboard is only for admin users.")
        
if __name__ == "__main__":
    main()
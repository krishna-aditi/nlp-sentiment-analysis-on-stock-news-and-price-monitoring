# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 22:31:39 2022

@author: krish
"""
import streamlit as st
# import matplotlib.pyplot as plt
import plotly.express as px
import yfinance as yf
import requests

# Plotly plot for high price
def price_plot(data_frame, comp):
    fig = px.line(data_frame, x="Date", y="High", labels={"Date": "Date",  "High": "High Price of Stock"}, width=750, height=500, template="plotly_dark")
    html_temp = f"""
        <div style="background-color:#154360;padding:2px">
        <h2 style="color:White;text-align:center;">Stock price monitor for {comp}</h2>
        </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    st.plotly_chart(fig)

# Dataframe for financial data
def comp_fin(info_summary_df, comp):
    html_temp = f"""
        <div style="background-color:#154360;padding:2px">
        <h2 style="color:White;text-align:center;">{comp} Quarterly Financials</h2>
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

# Company summary
def comp_summary(info, comp):
    html_temp = f"""
        <div style="background-color:#154360;padding:2px">
        <h2 style="color:White;text-align:center;">About {comp}</h2>
        </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    html_temp2 = f"""
        <div>
        <p style="color:white;align:"justify";">{info}</p>
        </div>
    """   
    st.markdown(html_temp2, unsafe_allow_html=True)

# Stock news
def comp_news(news, comp):
    html_temp = f"""
        <div style="background-color:#154360;padding:2px">
        <h2 style="color:White;text-align:center;">{comp} News</h2>
        </div>
    """
    st.markdown("")
    st.markdown(html_temp, unsafe_allow_html=True)
    html_temp2 = f' <div> <body style="color:white;align:"justify";">'  
    
    for n in news:
        if n['sentiment'] == 'POSITIVE':
            html_temp2 += f"<h2>{n['title']}</h2><p style='text-align:justify;'>{n['summary']} ...<a href='{n['url']}'>[Read Full Article]</a> </p> \n <p style='background-color:#27AE60;color:White;'><strong> News Sentiment: {n['sentiment']}</strong></p>"
        else:
            html_temp2 += f"<h2>{n['title']}</h2><p style='text-align:justify;'>{n['summary']} ...<a href='{n['url']}'>[Read Full Article]</a> </p> \n <p style='background-color:#7B241C;color:White;'><strong> News Sentiment: {n['sentiment']}</strong></p>"
    
    html_temp2 += "</body>  </div>"   
    st.markdown(html_temp2, unsafe_allow_html=True)
    
def main():
    html_temp_title = f"""
        <div style="background-color:SteelBlue;padding:4px">
        <h1 style="color:white;text-align:center;">NLP and Sentiment Analysis on Stock Market News with Price Monitoring Dashboard</h1>
        </div>
    """
    st.markdown(html_temp_title, unsafe_allow_html=True)
        
    page = st.sidebar.radio("Navigation Pane", ["Login page", "About the company", "Company news", "API Live Dashboard", "On-demand News Fetch for Admin"])
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
                token = requests.post("https://big-data-final-project-347804.ue.r.appspot.com/token", data = authjson)
                if col2.button("Log Out"):
                    s.authenticated = False
                    token = None
                    s.token = ''
                    s.company = ''
                    st.success(f"Log Out Successful!")
                    return None
                                
                if token.status_code == 200: 
                     s.authenticated = True
                     s.token = token.json()['access_token']
                     st.success(f"Login Successful! You now have access to explore other pages!")  
                else:
                    st.error('Please Enter Valid Username and Password!')
            else:
                st.error('Please Enter Valid Username and Password!')
                    
    if page == "About the company":
        if not s.authenticated:
            st.error(f"Please Login to Access this Page.")
        else:
            st.subheader("Choose company:")
            comp_name = st.selectbox("",("AAPL-Apple", "MSFT-Microsoft", "AMZN-Amazon", "WMT-Walmart", "GOOG-Alphabet", "FB-Meta", "TSLA-Tesla", "NVDA-NVIDIA", "PFE-Pfizer", "NFLX-Netflix"))
            s.company = ''
            comp = comp_name.split("-")[0].strip()
            params_test = {"company_name": comp}
            if st.button("Fetch"):
                s.company = comp_name.split('-')[-1].strip()
                headers = {"Authorization": f"Bearer {s.token}"}
                info_test = requests.post("https://big-data-final-project-347804.ue.r.appspot.com/stocks/stock_info", headers=headers, json = params_test)   
                if info_test.status_code == 200:
                    output = info_test.json()
                    # Lineplot for High column
                    if 'Error' in output.keys():
                        st.error(f"{output['Error']}")
                    else:
                        st.markdown("")
                        comp_summary(output['Info'], comp_name)
                        st.markdown("")
                        price_plot(output['Price'], comp_name)
                        st.markdown("")
                        comp_fin(output['Finance'], comp_name)
                        st.markdown("")
                else:
                    st.error(f"Server Error: {info_test.json()['detail']}")
    
    # Reads company news stored in bucket already
    if page == "Company news":
        headers = {"Authorization": f"Bearer {s.token}"}
        if s.company != '':
            params_test = {"company_name": s.company}
            response = requests.post("https://big-data-final-project-347804.ue.r.appspot.com/stocks/news", headers=headers, json = params_test)
            if response.status_code == 200:
                output = response.json()
                # Lineplot for High column
                if 'Error' in output.keys():
                    st.error(f"{output['Error']}")
                else:
                    comp_news(output['News'], s.company)
            else:
                st.error(f"Server Error: {response.json()['detail']}")
                    
        else:
            st.error("Please Select a Company and Fetch details in 'About Company' Page!!") 
    
    # Dashboard
    if page == "API Live Dashboard":
        html_temp_airflow = f"""
            <div style="background-color:#154360;padding:2px">
            <h2 style="color:White;text-align:center;">Stock API Live Dashboard</h2>
            </div>
        """
        st.markdown("")
        st.markdown(html_temp_airflow, unsafe_allow_html=True)
        headers = {"Authorization": f"Bearer {s.token}"}
        response = requests.post("https://big-data-final-project-347804.ue.r.appspot.com/stocks/dashboard", headers=headers)
        if response.status_code == 200:
            url = response.json()['url']
            st.markdown(f"""
                        <iframe width="700" height="550" src={url} frameborder="0" style="border:0" allowfullscreen></iframe>
                        """, unsafe_allow_html=True)
        else:
            st.error(f"Not an ADMIN! Stocks API Dashboard is only for ADMIN users.")
    
    # Generate news on-demand       
    if page == "On-demand News Fetch for Admin":
        html_temp_airflow = f"""
            <div style="background-color:#154360;padding:2px">
            <h2 style="color:White;text-align:center;">On Demand News Scrapper</h2>
            </div>
        """
        st.markdown("")
        st.markdown(html_temp_airflow, unsafe_allow_html=True)
        headers = {"Authorization": f"Bearer {s.token}"}
        st.subheader("Choose company:")
        comp_name = st.selectbox("",("AAPL-Apple", "MSFT-Microsoft", "AMZN-Amazon", "WMT-Walmart", "GOOG-Alphabet", "FB-Meta", "TSLA-Tesla", "NVDA-NVIDIA", "PFE-Pfizer", "NFLX-Netflix"))
        comp = comp_name.split("-")[-1].strip()
        params_test = {"company_name": comp}
        if st.button("Generate News"):
            response = requests.post("https://big-data-final-project-347804.ue.r.appspot.com/utils/getnews", headers=headers, json = params_test)
            if response.status_code == 200:
                if 'News' not in response.json().keys():
                    st.markdown(response.json())
                else:
                    url = response.json()['News']
                    st.markdown(f"""
                                {url}
                                """, unsafe_allow_html=True)
            else:
                st.error(f"Not an ADMIN! Triggering Stock News Scrapping is only for ADMIN users.")
        
if __name__ == "__main__":
    main()

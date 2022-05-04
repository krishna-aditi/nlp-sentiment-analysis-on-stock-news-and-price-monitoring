# -*- coding: utf-8 -*-
"""
Created on Tue May  3 10:24:29 2022

@author: krish
"""

from fastapi.testclient import TestClient

from stock_main import app

client = TestClient(app)

def test_token():
    response = client.post("https://big-data-final-project-347804.ue.r.appspot.com/token",
               headers={"Authorization": f"Basic Og=="},            
        json={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    assert type(response.json()['access_token']) == str

def test_home():
    response = client.get("https://big-data-final-project-347804.ue.r.appspot.com/")
    assert response.status_code == 200

def test_stock_home():
    response = client.get("https://big-data-final-project-347804.ue.r.appspot.com/stocks/")
    assert response.status_code == 200
    
def test_scrapper():
       
    response = client.post("https://big-data-final-project-347804.ue.r.appspot.com/utils/getnews",
        json={"company_name": "Amazon"}) 
    
    assert response.status_code == 200
    assert 'storage.cloud' in response.json()['News']

def test_news_read():
    
    response = client.post("https://big-data-final-project-347804.ue.r.appspot.com/stocks/news",
        json={"company_name": "Netflix"}) 
    
    assert response.status_code == 200 


def test_dashboard():

    response = client.post("https://big-data-final-project-347804.ue.r.appspot.com/stocks/dashboard")
    assert response.status_code == 200 
    assert 'datastudio.google' in response.json()['url']


def test_news_info():
    
    response = client.post("https://big-data-final-project-347804.ue.r.appspot.com/stocks/stock_info",
        json={"company_name": "AAPL"}) 
    
    assert response.status_code == 200 
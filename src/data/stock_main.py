# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 17:24:35 2022

@author: krish
"""

from fastapi import FastAPI
from pydantic import BaseModel # Pydantic is used for data handling
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from google.cloud import bigquery
import yfinance as yf
from news_scrapper import getNews
import os
import tempfile
import pandas as pd
import gcsfs
# User database
users_db = {
    "aditikrishna": {
        "username": "aditikrishna",
        "full_name": "Aditi Krishna",
        "email": "krishna.ad@northeastern.edu",
        "hashed_password": '$2b$12$A19ccgQBlxIDs8OsSyBQR.dSOFfOTY6WnyrA9GQDOs/oVDLaRMmf2',
        "disabled": False,
        "admin": False,
        "limit": 3
    },
    "admin": {
        "username": "admin",
        "full_name": "Administrator",
        "email": "krishna.ad@northeastern.edu",
        "hashed_password": '$2b$12$25DfJDB.uXAUBkVd7W1U2OKPk9q8yO4IGZEL77zLJjPFxrWf3q/Nm',
        "disabled": False,
        "admin": True,
        "limit": -1
    },
    "inactive": {
        "username": "inactive",
        "full_name": "Inactive User",
        "email": "krishna.ad@northeastern.edu",
        "hashed_password": '$2b$12$A19ccgQBlxIDs8OsSyBQR.dSOFfOTY6WnyrA9GQDOs/oVDLaRMmf2',
        "disabled": True,
        "admin": False,
        "limit": 3
    },
    "bigdata": {
        "username": "bigdata",
        "full_name": "Big Data",
        "email": "krishna.ad@northeastern.edu",
        "hashed_password": '$2b$12$A19ccgQBlxIDs8OsSyBQR.dSOFfOTY6WnyrA9GQDOs/oVDLaRMmf2',
        "disabled": False,
        "admin": False,
        "limit": 3
    },
    "mowgu": {
        "username": "mowgu",
        "full_name": "Mowgli Krishna",
        "email": "krishna.ad@northeastern.edu",
        "hashed_password": '$2b$12$A19ccgQBlxIDs8OsSyBQR.dSOFfOTY6WnyrA9GQDOs/oVDLaRMmf2',
        "disabled": False,
        "admin": False,
        "limit": 3
    }
}

# To sign the JWT token we need a secret key like a signature generate one by typing this in yout console " !openssl rand -hex 32 "
SECRET_KEY = 'a4e1f06420e88c39c20d056455c6dcab62f33b5c21761c8327599d0c6fd455ee' #signature to JWT
ALGORITHM = "HS256" #algorithm to validate JWT        
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # 30 minutes token validity time

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    admin: Optional[bool] = None
    limit: Optional[int] = None
    
class UserInDB(User):
    hashed_password: str

# Creating a passlib context to hash and verify passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Functions from https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create hashed password
def get_password_hash(password):
    return pwd_context.hash(password)

# Get user from database
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# Add new user to database with credentials
def add_user(username, full_name, email, password):    
    hashed = get_password_hash(password)
    users_db.update({username:{"username": f"{username}", "full_name":f"{full_name}", "email":f"{email}", "hashed_password":f"{hashed}"}})
    
# Create access token with time limit   
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Authenticate user
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def authenticate(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    
    except JWTError:
        raise credentials_exception
    
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(authenticate)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_admin(current_user: User = Depends(authenticate)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    if not current_user.admin:
        raise HTTPException(status_code=400, detail="Not an Admin User")
    return current_user

app = FastAPI()

# Endpoint for token verification
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

class StockParams(BaseModel):
    company_name: str

# General info about FastAPI
@app.get("/")
def read_main():
    return 'DAMG7245 Big Data Systems and Intelligent Analytics Final Project'

@app.get("/stocks/")
def read_stock():
    return 'NLP and Sentiment Analysis on Stock Market News with Price Monitoring Dashboard'

def writeDataToCloud(company, news_list):
    project_name = 'big-data-final-project'
    credentials = "big-data-final-project-347804-0935c4105776.json"
    FS = gcsfs.GCSFileSystem(project=project_name, token=credentials)
    try:
        temp = tempfile.NamedTemporaryFile(delete=False,mode='w',suffix='.txt') 
        with open(temp.name, "w", encoding="utf-8") as output:
            output.write(str((news_list)))
        FS.upload(temp.name, f'stock_news/{company}.txt')
        temp.close()
        os.unlink(temp.name)
        return FS.url(f'stock_news/{company}.txt').replace('googleapis','cloud.google')
    except Exception as e:
        raise Exception(f'Output Error: Error writing data to Google Cloud Bucket {e}')
        
def readDataFromCloud(company):
    project_name = 'big-data-final-project'
    credentials = "big-data-final-project-347804-0935c4105776.json"
    FS = gcsfs.GCSFileSystem(project=project_name, token=credentials)
    try:
        with FS.open(f'stock_news/{company}.txt', 'rb') as fp:
            json_ = eval(fp.read())
            return json_

    except Exception as e:
        raise Exception(f'Data Error: Could not find the file{e}')
        
# Endpoint to fetch company specific news
@app.post("/utils/getnews")
def scrape_news(params: StockParams, current_user: User = Depends(get_current_active_user)):
    
    print(f'{params.company_name}')
    try:
        headlines, news = getNews(params.company_name)
        url = writeDataToCloud(params.company_name, news)
        key = 'News'
        value = url
    except Exception as e:
        key = 'Error'
        value = f'Issue with fetching News: {e}'
    
    return {key:value}

# Endpoint to fetch company specific news
@app.post("/stocks/news")
def fetch_news(params: StockParams, current_user: User = Depends(get_current_active_user)):
    
    print(f'{params.company_name}')
    try:
        news = readDataFromCloud(params.company_name)
        key = 'News'
        value = news
    except Exception as e:
        key = 'Error'
        value = f'Issue with fetching News: {e}'
    
    return {key:value}
# Endpoint for admin live dashboard
@app.post("/stocks/dashboard") # authentication only for the admin
def dashboardURL(current_user: User = Depends(get_current_active_admin)):
    # To embed Data Studio Dashboard for user logging
    return {'url':'https://datastudio.google.com/embed/reporting/337d3400-d694-4124-a100-5de560154ac9/page/Xu1qC'}


# Endpoint for scraping with yfinanceAPI
@app.post("/stocks/stock_info")
def stock_info_scrape(params: StockParams, current_user: User = Depends(get_current_active_user)): # Receive whatever is in the body
    """
    **NLP and Sentiment Analysis on Stock Market News with Price Monitoring Dashboard**
    
    Submitted by - Team 2
    * Aditi Krishna
    * Abhishek Jaiswal
    * Sushrut Mujumdar
    """
    username = current_user.username
    company = params.company_name
    credentials_path = 'big-data-final-project-347804-0935c4105776.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    current_hits = 0
    today = datetime.now().strftime('%Y-%m-%d')
    # BigQuery table append
    bq_client = bigquery.Client()
    table = bq_client.get_table("{}.{}.{}".format('big-data-final-project-347804', 'stocks', 'user_log'))
    # Pass table name as "sevir-nlp.api_record.logs" 
    query= f"""SELECT API_call_count  FROM `big-data-final-project-347804.stocks.user_log` 
    WHERE Username= '{username}' AND DATE(In_time) = '{today}' ORDER BY API_call_count DESC LIMIT 1"""
    results = bq_client.query(query).result()
    for result in results:
        current_hits = result.API_call_count
    
    if current_user.limit > current_hits or current_user.limit < 0:
        pass
    else:
        return {"rate_limit_error": "Maximum tries reached!"}
    
    # To embed Data Studio Dashboard for user logging
    api_name = 'StocksNLP'
    intime = datetime.now()
    
    # Price
    try:
        data_frame = yf.download(company, start='2021-01-01', end=today, progress=False)
        data_frame = data_frame.reset_index()
        data_frame = data_frame.drop(columns = ["Low", "Adj Close", "Volume"])
        output_obj = data_frame.to_dict("records")
        
        # key = 'Output'
        # value = output_obj

        key_price = 'Price'
        value_price = output_obj

    except Exception as e:
        key_price = 'Error'
        value_price = f'Could not fetch Prices from Yahoo Finance API: {e}' 
        return {key_price:value_price}

    # Financials
    try:        
        comp_stock = yf.Ticker(company)
        fin = comp_stock.quarterly_financials
        
        # Dataframe manipulation
        fin.columns = pd.to_datetime(fin.columns).strftime('%m/%d/%Y')
        fin = fin.reset_index()
        
        # Drop rows with NA values
        fin = fin.dropna()
        
        # Renaming columns
        fin.rename(columns = {'index':''}, inplace = True)
        fin = fin.to_dict("records") # datafram to dict
        
        key_fin = 'Finance'
        value_fin = fin
        
    except Exception as e:
        key_fin = 'Error'
        value_fin = f'Could not fetch Company Finances from Yahoo Finance API: {e}'
        return {key_fin:value_fin}
    
    # Company summary
    try: 
        about = comp_stock.info
        about = about['longBusinessSummary'] # str
        
        key_info = 'Info'
        value_info = about
    
    except Exception as e:
        key_info = 'Error'
        value_info = f'Could not fetch Information from Yahoo Finance API: {e}'
        return {key_info:value_info}
    
    outtime = datetime.now()
    totalproctime = (outtime-intime).seconds
    api_call_count = current_hits+1
    table = bq_client.get_table("{}.{}.{}".format('big-data-final-project-347804', 'stocks', 'user_log'))
    status = 'Success'
    
    rows_to_insert = [
    {u'Username':username,u'API_name':api_name, u'In_time':intime.strftime('%Y-%m-%d %H:%M:%S'), u'Out_time': outtime.strftime('%Y-%m-%d %H:%M:%S'), 
     u'Status':status, u'API_call_count': api_call_count, u'Processing_time': totalproctime, u'Stock_Name': company}
    ]
    
    errors = bq_client.insert_rows_json(table, rows_to_insert)
    if errors != []:
        key = 'fatal_error'
        value = f'Fatal Issue as User Logging on BigQuery Failed: {errors}'
        return {key:value}
    
    # return {key:value}
    return {key_price:value_price, key_fin:value_fin, key_info:value_info}
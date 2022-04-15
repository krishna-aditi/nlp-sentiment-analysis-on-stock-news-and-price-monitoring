Stock-price-prediction-and-nlp-pipeline
==============================

#### Overview
Prediction and analysis of the stock market are some of the most difficult tasks to execute. There are a multitude of reasons for this, including market volatility and a variety of other dependent and independent variables that influence the market value of a particular stock. Because of these factors, it is extremely difficult for any stock market expert to predict the market's rise and fall with great accuracy. 

#### Goals 
Goal is to curate all company specific information in one place so as to help the user make an informed decision regarding trading

1. Aim is to create a workflow where we curate the data by web-scraping using YFinance library in Python. 
2. The model will be trained using the Long Short Term Memory(LSTM) model, to provide short term recommendations to buy or sell a stock of the company chosen by the user.
3. The interface will include a dashboard with the stock trend for the company. We also aim to create an NLP pipeline for company specific news that will also be web-scraped. 
4. A summarized version of the news will be reflected on the interface, and the associated sentiment with it

#### Use cases
1. Recommendation: The system can recommend the stock to trade(buy or sell), so an investor can maximize the profit
2. Predication: System will predict the price of the specific stock on a short term
3. Outline: System will show the stock-related news summary which will help the investor to make informed decisions
4. Single hub for stock news and company profile

#### Data
Following libraries will be potentially used to web-scrape data off Yahoo Finance:
1. yfinance 
2. BeautifulSoup (bs4)
3. yahoofinancials

#### Sample code
```
import requests 
from bs4 import BeautifulSoup 
import json

mystocks = ['AAPL','TWTR'] 
stockdata = []

def getData( symbol):
    headers= { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15'} 
    url = f'https://finance.yahoo.com/quote/{symbol}' 
    r = requests.get(url, headers=headers) 
    soup = BeautifulSoup(r.text, 'html.parser') 
    stock = {
    'symbol': symbol, 
    'price': soup.find('div', {'class':'D(ib) Mend(20px)'}).find_all('span')[0].text, 
    'change': soup.find('div', {'class':'D(ib) Mend(20px)'}).find_all('span')[1]. text,
    }
    return stock

for item in mystocks:
    stockdata.append(getData(item)) 
    print('Getting:', item)
with open('stockdata.json', 'w') as f:
    json. dump(stockdata, f)
```

#### Process Outline
- Developing an API for data scraping for stock information and profile, as well as stock news
- Data preprocessing
- Scheduling jobs to scrape data using Airflow
- Using pre-trained ML model for price prediction
- Dashboard creation
- Building lambda functions for news summarization 
- Building lambda functions for sentiment analysis
- Deploying Lambda functions using AWS ECR
- Developing UI using Streamlit, deploy on Streamlit Cloud

#### Deployment Details:
1. Language: Python
2. Container: Docker, AWS ECR, AWS
3. Cloud ecosystems: AWS, Google cloud platform
4. Cloud tools: AWS Lambda, AWS Cloudwatch, AWS Gateway, AWS Quicksight, AWS Sagemaker, AWS S3, AWS DynamoDB/Redshift, GCP cloud storage, Google BigQuery, Google App Engine, Google DataStudio
5. Tools for analysis: Google Colab, Anaconda Spyder, Microsoft Azure Visual Studio
6. Other tools and frameworks: FastAPI, Pytest, Streamlit, Airflow

#### High-level workflow

![image](https://github.com/krishna-aditi/Stock-price-prediction-and-nlp-pipeline/blob/main/reports/figures/High-level%20workflow.png)

Fig. Proposed high-level workflow

#### References:
1. https://python.plainenglish.io/build-a-stock-data-api-using-web-scraping-and-fastapi-dcbcdbd3d2ec
2. https://zzhu17.medium.com/web-scraping-yahoo-finance-news-a18f9b20ee8a
3. https://www.analyticsvidhya.com/blog/2021/06/download-financial-dataset-using-yahoo-finance-in-python-a-complete-guide/
4. https://www.parsehub.com/blog/scrape-yahoo-finance/

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

Stock-price-prediction-and-nlp-pipeline
==============================

Proposal link (CLAAT): https://codelabs-preview.appspot.com/?file_id=1x528Ez7oU1SrBOJBMSHLpZ-h7VmKvegiq2tCO8b5fQw#1

#### Overview
Stock market analysis is a difficult task to execute because of market volatility and a multitude of  other dependent and independent factors that influence the market value of a particular stock. One of these factors - investor sentiment, is very much capable of influencing the stock price. News and social media are few of the ways to capture it. We aim to bring together natural language processing and sentiment analysis of the stock related news to better understand the stock price trends.

#### Goals 
Goal is to curate company specific news in a single interface, along with their stock trends with the help of a live dashboard. We focus on summarizing the news using NLP models, and labeling it as positive or negative using sentiment analysis. A dashboard with most recent data will also be present so as to help the user make an informed decision regarding trading.

1. Create a workflow where we curate the data by web-scraping using YFinance library in Python
2. The Streamlit interface will have an embedded dashboard for stock trends (high prices), built using Plotly. The page also includes stock specific quarterly financials and a description about the company
3. Set up an Airflow DAG:
    - Web-scrape stock news using NewsAPI
    - Run AWS Lambda function for summarization 
    - Run AWS Lambda function for sentiment analysis
4. The final data will be cached in the GCP Cloud Storage Bucket for the user to trigger a "fetch" operation on the Streamlit application

#### Use cases
1. Single hub for stock trends and associated news to help the investor to make informed decisions
2. Platform for learning about company stocks, or, stock  market analysis

#### Data
Following libraries will be potentially used to web-scrape data off Yahoo Finance:
1. yfinance 
2. BeautifulSoup (bs4)
3. news-api

#### Process Outline
- FastAPI for data scraping for stock prices
- JWT Authentication for FastAPI
- Data scraping for stock news
- Dashboard creation using Google Data Studio
- Building lambda functions for news summarization 
- Building lambda functions for sentiment analysis
- Deploying Serverless lambda 
- Developing UI using Streamlit
- Deploy on Streamlit Cloud

#### Deployment Details:
1. Language: Python
2. Container: Docker, AWS ECR
3. Cloud ecosystems: AWS, Google cloud platform
4. Cloud tools: AWS Lambda, AWS Cloudwatch, AWS Gateway, GCP cloud storage, Google BigQuery, Google App Engine, Google DataStudio
5. Tools for analysis: Google Colab, Anaconda Spyder, Microsoft Azure Visual Studio
6. Other tools and frameworks: FastAPI, Pytest, Streamlit, Airflow

#### High-level workflow

![image]()

Fig. Proposed  workflow

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

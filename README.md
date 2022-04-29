NLP and Sentiment Analysis on Stock News and Price Monitoring
==============================

Proposal link (CLAAT): https://codelabs-preview.appspot.com/?file_id=1x528Ez7oU1SrBOJBMSHLpZ-h7VmKvegiq2tCO8b5fQw#1

#### Overview
Stock market analysis is a difficult task to execute because of market volatility and a multitude of  other dependent and independent factors that influence the market value of a particular stock. One of these factors - investor sentiment, is very much capable of influencing the stock price. News and social media are few of the ways to capture it. We aim to bring together Natural Language Processing and Sentiment Analysis of the stock related news to better understand the stock price trends.

#### Goals 
Goal is to create a platform with curated information about a company's profile, stock specific news (from 24 hours), and the stock price trend from the past year. We focus on summarizing the news using NLP models, and labeling it as positive or negative using sentiment analysis. The platform aims to help the user make informed trading decisions.

1. Create a workflow to web-scrape company specific information using YFinance library in Python
2. Build a Streamlit interface for the FastAPI to render stock price trends, company’s financials, and description of the business
3. Create an Airflow DAG to do the following:
4. Web-scrape company specific stock news with the help of NewsAPI and Newspaper3K API
5. Call the Summarization API (Lambda function) for summarization on each news article’s content
6. Call Sentiment Analysis API (Lambda function) for extracting the sentiment of each news article
7. Summarized news, along with the associated sentiment will be rendered on the Streamlit

#### Main Requirements
To test pretrained models and train API requires 
- Python 3.8
- pandas
- numpy
- Streamlit
- Python-jose
- Passlib
- Transformers 3.4
- Torch
- GCSFS
- Plotly
- Yfinance
- NewsAPI
- Newspaper3K

#### Use cases
1. Single hub for stock trends and associated news to help the investor to make informed decisions
2. Platform for learning about company stocks, or, stock  market analysis

#### Data
Following libraries will be potentially used to web-scrape data off Yahoo Finance:
1. yfinance 
2. BeautifulSoup (bs4)
3. news-api
4. newspaper3k

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
4. Cloud tools: AWS Lambda, AWS Cloudwatch, AWS Gateway, GCP Cloud Storage, Google BigQuery, Google App Engine, Google DataStudio
5. Tools for analysis: Google Colab, Anaconda Spyder, Microsoft Azure Visual Studio
6. Other tools and frameworks: FastAPI, Pytest, Streamlit, Airflow

#### High-level workflow

![image](https://github.com/krishna-aditi/nlp-sentiment-analysis-on-stock-news-and-price-monitoring/blob/main/reports/figures/Proposed_architecture.png)

Fig. Proposed  workflow

#### References:
1. https://python.plainenglish.io/build-a-stock-data-api-using-web-scraping-and-fastapi-dcbcdbd3d2ec
2. https://zzhu17.medium.com/web-scraping-yahoo-finance-news-a18f9b20ee8a
3. https://www.analyticsvidhya.com/blog/2021/06/download-financial-dataset-using-yahoo-finance-in-python-a-complete-guide/
4. https://www.parsehub.com/blog/scrape-yahoo-finance/
5. https://newspaper.readthedocs.io/en/latest/
6. https://huggingface.co/blog/sentiment-analysis-python
7. https://newsapi.org/docs/client-libraries/python

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
    │   │   └── stock_main.py
    |   │   ├── news_scrapper.py
    |   │   ├── streamlit-app.py
    |   │   ├── airflow_dag
    |   │   │   └── news_airflow.py
    │   │   ├── news_summary
    |   |   │   ├── handler.py
    |   |   │   ├── get_models.py
    |   │   |   ├── dockerfile
    |   |   │   ├── serverless.yaml
    |   |   │   └── requirements.txt
    |   |   |
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │                     predictions
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

#### Submitted by:

![image](https://user-images.githubusercontent.com/37017771/153502035-dde7b1ec-5020-4505-954a-2e67528366e7.png)

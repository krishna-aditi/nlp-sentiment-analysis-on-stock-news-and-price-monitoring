# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 16:39:29 2022

@author: krish
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path
sys.path.append(os.path.join(Path.home(),'finalProject'))
from news_scrapper import getAllNews

def print_status():
    print('Successfully run News Scrapping Schedule Run')
    return 'Successfully run News Scrapping Schedule Run'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
  }

with DAG(dag_id='stock_news_scrapper', default_args=default_args, schedule_interval='@daily',catchup=False) as dag:

    # When running independently (For testing using API directly)
    t1 = PythonOperator(task_id='news_cache',
                   python_callable = getAllNews)
    
    # Printing Status for debug
    t2 = PythonOperator(task_id='status_check',
                   python_callable=print_status)

    t1 >> t2

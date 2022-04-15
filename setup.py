from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Aim is to create a workflow where we curate the data by web-scraping in Python. The model will be trained using the Long Short Term Memory(LSTM) model, to provide short term recommendations to buy or sell a stock of the company chosen by the user. The interface will include a dashboard with the stock trend for the company. We also aim to create an NLP pipeline for stock specific news that will also be web-scraped. A summarized version of the news will be reflected on the interface, and the associated sentiment with it. Goal is to curate all company specific information in one place so as to help the user make an informed decision regarding trading.',
    author='Aditi Krishna',
    license='MIT',
)

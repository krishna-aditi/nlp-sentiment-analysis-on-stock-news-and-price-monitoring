# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:09:06 2022

@author: krish
"""

from transformers import T5ForConditionalGeneration, T5Tokenizer
import json

# import os
# import pathlib
# abspath = pathlib.Path(__file__).parent.resolve()

def serverless_pipeline():
    # initialize the model architecture and weights
    model = T5ForConditionalGeneration.from_pretrained("./model")
    # initialize the model tokenizer
    tokenizer = T5Tokenizer.from_pretrained("./model")

    def summary(news_text):
        # encode the text into tensor of integers using the appropriate tokenizer
        news_inputs = tokenizer.encode("summarize: " + news_text, return_tensors="pt", max_length = 350, truncation=True)
        # generate the summarization episode output
        news_outputs = model.generate(
                news_inputs, 
                max_length=250, 
                min_length=100, 
                length_penalty=2.0, 
                num_beams=4, 
                early_stopping=True)
        # just for debugging
        news_summary = tokenizer.decode(news_outputs[0])
        print(f"News Summary: {news_summary}")
        return news_summary
    return summary
    
# initializes the pipeline
summarize_pipeline = serverless_pipeline()

# handler
def handler(event, context):
    try:
        # loads the incoming event into a dictonary
        article = json.loads(event['body'])
        print('Printing event for debugging: ',article)
        news_text = article['content']
        
        print(f'summarize_pipeline({news_text})')
        # uses the pipeline to predict the answer
        news_summary = summarize_pipeline(news_text)
        # article['summary'] = news_summary
        print(f"news_summary:{news_summary}")
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({"news_summary": news_summary})
        }
    except Exception as e:
        print("Check ECR error here: ",repr(e))
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": repr(e)
        }

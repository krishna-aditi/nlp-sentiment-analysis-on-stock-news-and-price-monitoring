import json
import dateutil.parser 
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
     
def serverless_pipeline(model_path='./model'):

    """Initializes the model and tokenzier and returns a predict function that ca be used as pipeline"""
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    sentiment = pipeline("sentiment-analysis",model=model,tokenizer=tokenizer)
    def predict(statement):
        ner_results = sentiment(statement)
        return ner_results
    return predict

question_answering_pipeline = serverless_pipeline()

# initializes the pipeline
def handler(event, context):
    try:
        # loads the incoming event into a dictonary
        body = json.loads(event['body'])
        print(body)
        answer = question_answering_pipeline(statement=body['context'])
        print(answer)
        # uses the pipeline to predict the answer
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True

            },
            "body": json.dumps({'answer': answer})
        }
    except Exception as e:
        print(repr(e))
        return {
            "statusCode": 500,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({"error": repr(e)})
        }
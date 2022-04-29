from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import json

def serverless_pipeline():
    # initialize the model architecture and weights
    model = AutoModelForSequenceClassification.from_pretrained("./model")

    # initialize the model tokenizer
    tokenizer = AutoTokenizer.from_pretrained("./model")
    
    def sentiment(news_text):
        sentimentanalyzer = pipeline("sentiment-analysis", model = model, tokenizer = tokenizer)
        news_sentiment_result = sentimentanalyzer(news_text)[0]
        sentiment_value = news_sentiment_result['label']
        print(f"News sentiment: {sentiment_value}")
        return sentiment_value
    return sentiment
    
# initializes the pipeline
sentiment_pipeline = serverless_pipeline()

# handler
def handler(event, context):
    try:
        # loads the incoming event into a dictonary
        article = json.loads(event['body'])
        print('Printing event for debugging: ',article)
        news_text = article['content']
        print(f'sentiment_pipeline({news_text})')
        # uses the pipeline to predict the answer
        news_sentiment = sentiment_pipeline(news_text)
        print(f"news_sentiment:{news_sentiment}")
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps({"sentiment": news_sentiment})
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

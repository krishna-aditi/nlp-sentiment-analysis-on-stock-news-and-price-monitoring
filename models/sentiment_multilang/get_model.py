from transformers import AutoTokenizer, AutoModelForSequenceClassification

def get_model(model):
  """Loads model from Hugginface model hub"""
  try:
    model = AutoModelForSequenceClassification.from_pretrained(model)
    model.save_pretrained('./model')
  except Exception as e:
    raise(e)

def get_tokenizer(tokenizer):
  """Loads tokenizer from Hugginface model hub"""
  try:
    tokenizer = AutoTokenizer.from_pretrained(tokenizer)
    tokenizer.save_pretrained('./model')
  except Exception as e:
    raise(e)

get_model("nlptown/bert-base-multilingual-uncased-sentiment")
get_tokenizer("nlptown/bert-base-multilingual-uncased-sentiment")
from transformers import T5ForConditionalGeneration, T5Tokenizer

def get_model(model):
  """Loads model from Hugginface model hub"""
  try:
    model = T5ForConditionalGeneration.from_pretrained(model)
    model.save_pretrained('./model')
  except Exception as e:
    raise(e)

def get_tokenizer(tokenizer):
  """Loads tokenizer from Hugginface model hub"""
  try:
    tokenizer = T5Tokenizer.from_pretrained(tokenizer)
    tokenizer.save_pretrained('./model')
  except Exception as e:
    raise(e)

get_model("t5-base")
get_tokenizer("t5-base")

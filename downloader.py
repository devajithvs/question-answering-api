from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering
import os

if __name__ == '__main__':
    print("Downloading...")
    os.mkdir("/content/model/")
	tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
	tokenizer.save_pretrained("/content/model")
	model = TFAutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")
	model.save_pretrained("/content/model")
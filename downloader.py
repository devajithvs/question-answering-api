from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
import os
os.mkdir("/model/")

if __name__ == '__main__':
    print("Downloading...")
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
    tokenizer.save_pretrained("/model")
    model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")
    model.save_pretrained("/model")
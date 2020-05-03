import os
import pandas as pd
from ast import literal_eval
from cdqa.utils.filters import filter_paragraphs
from cdqa.pipeline import QAPipeline
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.engines.bing import Search as BingSearch

def get_answer(query, df):
  cdqa_pipeline = QAPipeline(reader='./models/distilbert_qa.joblib')
  cdqa_pipeline.fit_retriever(df=df)
  prediction = cdqa_pipeline.predict(query)
  print('query: {}'.format(query))
  print('answer: {}'.format(prediction[0]))
  # print('title: {}'.format(prediction[1]))
  print('paragraph: {}'.format(prediction[2]))

def pad_dict_list(dict_list, padel):
    lmax = 0
    for lname in dict_list.keys():
        lmax = max(lmax, len(dict_list[lname]))
    for lname in dict_list.keys():
        ll = len(dict_list[lname])
        if  ll < lmax:
            dict_list[lname] += [padel] * (lmax - ll)
    return dict_list

def search_google(query):
  search_args = (query, 0)
  dsearch = GoogleSearch()
  dresults = dsearch.search(*search_args)
  if dresults["direct_answer"]:
    answer = dresults["direct_answer"]
    print(f"Question: {query}")
    print(f"Answer: {answer}\n")
  else:
    dict = {"title":dresults["titles"], "paragraphs":[[i] for i in dresults["descriptions"]]}
    dict = pad_dict_list(dict, "[]")
    df = pd.DataFrame(dict) 
    df.to_csv('file1.csv') 
    df = pd.read_csv('file1.csv', converters={'paragraphs': literal_eval})
    get_answer(query, df)

def search_bing(query):
  search_args = (query, 0)
  dsearch = BingSearch()
  dresults = dsearch.search(*search_args)
  dict = {"title":dresults["titles"], "paragraphs":[[i] for i in dresults["descriptions"]]}
  dict = pad_dict_list(dict, "[]")
  df = pd.DataFrame(dict)
  df.to_csv('file1.csv') 
  df = pd.read_csv('file1.csv', converters={'paragraphs': literal_eval})
  get_answer(query, df)

if __name__ == '__main__':
    print("Working")

    query = 'Who got the 1st or 2nd medal?'
    search_google(query)
    search_bing(query)
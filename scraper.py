from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering
import tensorflow as tf

from search_engine_parser.core.engines.google import Search as GoogleSearch

from googletrans import Translator
import os

print("Working")
print(os.listdir())
model = TFAutoModelForQuestionAnswering.from_pretrained('model')
tokenizer = AutoTokenizer.from_pretrained("model")

def get_answer(query, context):
    inputs = tokenizer.encode_plus(query, context, add_special_tokens=True, return_tensors="tf")
    input_ids = inputs["input_ids"].numpy()[0]

    text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
    answer_start_scores, answer_end_scores = model(inputs)

    # Get the most likely beginning of answer with the argmax of the score
    answer_start = tf.argmax(answer_start_scores, axis=1).numpy()[0]

    # Get the most likely end of answer with the argmax of the score
    answer_end = (tf.argmax(answer_end_scores, axis=1) + 1).numpy()[0]

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    print(f"Question: {query}")
    print(f"Answer: {answer}\n")
    return answer

def translate(question):
    translator = Translator()
    question = question.replace('.', '')
    query = translator.translate(question).text
    query += ''
    return query

def search_google(query):
    dsearch = GoogleSearch()
    dresults = dsearch.search(query, 0)
    if dresults["direct_answer"]:
        answer = dresults["direct_answer"]
        print(f"Question: {query}")
        print(f"Answer: {answer}\n")
        return answer
    else:
        context = ' '.join(dresults["descriptions"][0:5])
        context = context.replace('...', '')
        return get_answer(query, context)

def search_google_native_lang(query):
    search_args = (query, 0)
    dsearch = GoogleSearch()
    dresults = dsearch.search(*search_args)
    context = ' '.join(dresults["descriptions"][0:2])
    context = context.replace('...', '')
    context = translate(context)
    answer = dresults["titles"][0].replace('...', '') + "\n" + dresults["descriptions"][0].replace('...', '')
    return [answer, get_answer(translate(query), context)]

def solution(question):
    query = translate(question)
    answer_native = search_google_native_lang(question)
    answers = dict();
    answers['first_result'] = answer_native[0]
    answers['translate_result'] = answer_native[1]
    answers['google'] = search_google(query)
    return answers 
from transformers import AutoTokenizer, TFAutoModelForQuestionAnswering
import tensorflow as tf

from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.engines.bing import Search as BingSearch

from googletrans import Translator

def get_answer(query, context):
      inputs = tokenizer.encode_plus(query, context, add_special_tokens=True, return_tensors="tf")
      input_ids = inputs["input_ids"].numpy()[0]

      text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
      answer_start_scores, answer_end_scores = model(inputs)

      answer_start = tf.argmax(
          answer_start_scores, axis=1
      ).numpy()[0]  # Get the most likely beginning of answer with the argmax of the score
      answer_end = (
          tf.argmax(answer_end_scores, axis=1) + 1
      ).numpy()[0]  # Get the most likely end of answer with the argmax of the score

      answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

      print(f"Question: {query}")
      print(f"Answer: {answer}\n")
      return answer

if __name__ == '__main__':
    print("Working")

    model = TFAutoModelForQuestionAnswering.from_pretrained('/content/model')
    tokenizer = AutoTokenizer.from_pretrained("/content/model")

    translator = Translator()
    question = '"വീടുകൾക്കുള്ളിൽ അവധിക്കാലം ചെലവഴിക്കാൻ നിർബന്ധിതരായ കുട്ടികളുടെ സർഗാത്മകത പ്രകാശിപ്പിക്കുന്നതിന് സംസ്ഥാന പൊതുവിദ്യാഭ്യാസ വകുപ്പ് രൂപം നൽകിയ പദ്ധതി?'
    question = question.replace('.', '')
    query = translator.translate(question).text
    query += ''
    search_args = (query, 0)

    dsearch = GoogleSearch()
    dresults = dsearch.search(*search_args)
    context = " "
    if dresults["direct_answer"]:
      answer = dresults["direct_answer"]
      print(f"Question: {query}")
      print(f"Answer: {answer}\n")
      print()
    else:
      context = ' '.join(dresults["descriptions"][0:3])
      context = context.replace('...', '')

      answer = get_answer(query, context)
      print(answer)

    bsearch = BingSearch()
    bresults = bsearch.search(*search_args)
    context = ' '.join(bresults["descriptions"][0:3])
    context = context.replace('...', '')

    answer = get_answer(query, context)
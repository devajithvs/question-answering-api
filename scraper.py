from search_engine_parser.core.engines.bing import Search as  BingSearch
from search_engine_parser.core.engines.google import Search as GoogleSearch
    
from googletrans import Translator
translator = Translator()

from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

if __name__ == '__main__':
    print("Working")
    model = AutoModelForQuestionAnswering.from_pretrained('/model')
    tokenizer = AutoTokenizer.from_pretrained("/model")

    def get_answer( query, context):
        inputs = tokenizer.encode_plus(query, context, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]
        text_tokens = tokenizer.convert_ids_to_tokens(input_ids)
        answer_start_scores, answer_end_scores = model(**inputs)

        answer_start = torch.argmax(
            answer_start_scores
        )  # Get the most likely beginning of answer with the argmax of the score
        answer_end = torch.argmax(answer_end_scores) + 1  # Get the most likely end of answer with the argmax of the score

        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

        print(f"Question: {query}")
        print(f"Answer: {answer}\n")
        return answer

    question = '"വീടുകൾക്കുള്ളിൽ അവധിക്കാലം ചെലവഴിക്കാൻ നിർബന്ധിതരായ കുട്ടികളുടെ സർഗാത്മകത പ്രകാശിപ്പിക്കുന്നതിന് സംസ്ഥാന പൊതുവിദ്യാഭ്യാസ വകുപ്പ് രൂപം നൽകിയ പദ്ധതി?'
    print(question)
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
    print(context)
    bsearch = BingSearch()
    bresults = bsearch.search(*search_args)
    context = ' '.join(bresults["descriptions"][0:3])
    context = context.replace('...', '')
    print(context)

    answer = get_answer(query, context)
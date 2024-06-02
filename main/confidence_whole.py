import json
import os
import re
import openai
# pylint: disable=g-bad-import-order
from common import data_loader
from common import modeling
from common import shared_config
from common import utils
from common.template import OPEN_SOURCE_TEMPLATE
from main import config as main_config
from main import methods
from main.prompt import WHOLE_SELF_CONF_FORMAT_CONTINUE, SELF_CONF_FORMAT_CONTINUE, CRITERION_CONTINUE

openai.api_base = 'https://hb.rcouyi.com/v1'
os.environ["HTTP_PROXY"] = "http://10.61.3.12:7788"
os.environ["HTTPS_PROXY"] = "http://10.61.3.12:7788"

SAFE_result_path='./results/vicuna-7b_SAFE.json'

# resume_result_path = './results/selfconf-llama_2_7b.json'
resume_result_path = None
RESUME_BREAK_POINT = None

def check_model_consistency(model_name, path):
    path = path.split("/")[-1].split("_SAFE")[0]
    if path == model_name:
        print("Consistency Checked")
    else:
        print("Error: Not Consistent")
        exit(0)

def print_config(model_name: str, model: modeling.Model) -> None:
  """Prints out the current configuration of experiments."""
  utils.print_info(f'{model_name} settings.')
  model.print_config()
  print()


check_model_consistency(main_config.responder_model_short, SAFE_result_path)

if main_config.responder_model in OPEN_SOURCE_TEMPLATE:
    path = os.path.join(main_config.path,main_config.responder_model)
    device = main_config.device
else:
    path = None
    device = None


responder = modeling.Model(
    model_name=main_config.responder_model,
    temperature=0.1,
    max_tokens=1024,
    show_responses=main_config.show_responder_responses,
    show_prompts=main_config.show_responder_prompts,
    path = path,
    device = device
)
print_config('Responder', responder)


with open(SAFE_result_path, 'r') as file:
    json_data = json.load(file)

# print(json_data["per_prompt_data"][29])
# exit(0)

# for i, data in enumerate(json_data["per_prompt_data"]):
#     try:
#         print(i)
#         data_dict={}
#         question = data["side2_posthoc_eval_data"]["prompt"]
#         response = data["side2_posthoc_eval_data"]["response"]
#         checked_statements = data["side2_posthoc_eval_data"]["checked_statements"]

#         statements_list=[]
#         for item in checked_statements:
#             fact_dict = {}
#             fact = item["self_contained_atomic_fact"]
#             relevance = re.compile(r'Not Foo|Foo').search(item["relevance_data"]["is_relevant"]).group()
#             correctness = item["annotation"]
#             print(f"{fact} Is Relevant: {relevance}, Annotation: {correctness}")
#     except:
#         exit(0)
# exit(0)


if resume_result_path:
    with open(resume_result_path) as f:
        return_list=json.load(f)

    break_point = RESUME_BREAK_POINT
    should_begin=False

    for index, data in enumerate(json_data["per_prompt_data"]):

        if index<break_point:
            continue
        
        question = data["side2_posthoc_eval_data"]["prompt"]

        # if 'Arduino Uno board' in question:
        #     print(index)
        #     print(return_list[-1]["question"])
        #     print('\n',question)

        #     print(return_list[-1]["question"] == question)
        #     exit(0)
        # else:
        #     continue

        if question == return_list[-1]["question"]:
            print("it is the last, setting should_begin=True..")
            should_begin=True
            break
        else:
            print("wrong last, should not begin\n")
            print("question",question,'\n')
            print("list",return_list[-1]["question"])
            exit(0)

    if should_begin:
        print("start..")
    else:
        exit(0)
else:
    return_list = []



for index, data in enumerate(json_data["per_prompt_data"]):

    if resume_result_path:
        if index < break_point+1:
            continue
    
    print("\n\n=====index:",index)
    wrong_question_list=[]
    data_dict={}
    question = data["side2_posthoc_eval_data"]["prompt"]
    response = data["side2_posthoc_eval_data"]["response"]

    self_confidence_prompt = WHOLE_SELF_CONF_FORMAT_CONTINUE.format(criterion=CRITERION_CONTINUE, question=question,response=response)
    self_confidence_response = responder.generate(self_confidence_prompt)
    self_confidence_score = re.findall(r'\[\d\.\d{2}\]', self_confidence_response)


    # print(data["side2_posthoc_eval_data"])
    try:
        print(question)
        print(response)
        data_dict["correctness"] = float(data["side2_posthoc_eval_data"]["Supported"])/float(data["side2_posthoc_eval_data"]["num_claims"])
        data_dict["question"] = question
        data_dict["response"] = response
        data_dict["confidence"] = {"score":self_confidence_score,"response":self_confidence_response}


        print(data_dict["correctness"])
        print(data_dict["confidence"]["score"])
        print(data_dict["confidence"]["response"])
        return_list.append(data_dict)
    except:
        wrong_question_list.append(index)
        data_dict["question"] = question
        data_dict["response"] = response
        return_list.append(data_dict)
        print("WRONG!!!!!") # 13b 453 wrong
    
    with open('./results/{}_NOFACT_CONF.json'.format(main_config.responder_model_short), 'w') as outfile:
        json.dump(return_list, outfile)

print("WRONG:",wrong_question_list)

    







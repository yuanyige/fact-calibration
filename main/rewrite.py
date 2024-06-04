import os
import json
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re
import numpy as np 

from absl import app

from common import data_loader
from common import modeling
from common import shared_config
from common import utils
from common.template import OPEN_SOURCE_TEMPLATE
from main import config as main_config
from main import methods
from main.prompt import *

result_path = './results/gpt_35_turbo_FACT_CONF.json'
number_of_samples=500
resume_result_path = None
RESUME_BREAK_POINT = None

model_name = result_path.split('/')[-1].replace(".json","").split('_CONF')[0]
print('model_name',model_name)

def check_model_consistency(model_name, path):
    if 'gpt_35' in path:
        path = path.split("/")[-1].split("o")[0]+'o'
    else:
        path = path.split("/")[-1].split("b")[0]+'b'
    if path == model_name:
        print("Consistency Checked")
    else:
        print("Error: Not Consistent")
        print(model_name)
        print(path)
        exit(0)

def print_config(model_name: str, model: modeling.Model) -> None:
  """Prints out the current configuration of experiments."""
  utils.print_info(f'{model_name} settings.')
  model.print_config()
  print()


def run(path, model):
    with open(path) as f:
        results = json.load(f)

    return_list = []
    for index, sentence in enumerate(results):
        sentence["revise"]=[]
        if index >= number_of_samples:
            break

        confidence_vector=[]
        num_facts = 0

        for item in sentence["statements"]:

            ret_dict={}
            
            score2 = re.findall(r'\d\.\d{2}', item["confidence"]["response"])
            if len(item["confidence"]["score"])!=0:
                score1 = re.findall(r'\d\.\d{2}', item["confidence"]["score"][0])
                confident_score=float(score1[0])
                num_facts = num_facts + 1
            elif len(score2)!=0:
                confident_score=float(score2[0])
                num_facts = num_facts + 1
            else:
                print("WRONG #1!!")
            
            confidence_vector.append(float(confident_score))

        confidence_vector=np.array(confidence_vector)
        

        if confidence_vector.std() > 0:

            mean_value = confidence_vector.mean()
            low_indices = np.where(confidence_vector < mean_value)
            high_indices = np.where(confidence_vector >= mean_value)
            #response = [sentence["statements"][i]["fact"]+":" + str(sentence["statements"][i]["confidence"]["score"][0]) for i in range(len(sentence["statements"]))]
            #low_confidence_facts = list(map(lambda i: sentence["statements"][i]["fact"]+":"+str(sentence["statements"][i]["confidence"]["score"][0]), low_indices[0]))
            #high_confidence_facts = list(map(lambda i: sentence["statements"][i]["fact"]+":"+str(sentence["statements"][i]["confidence"]["score"][0]), high_indices[0]))

            try:
                low_confidence_facts = list(map(lambda i: sentence["statements"][i]["fact"], low_indices[0]))
                low_confidence_score = list(map(lambda i: sentence["statements"][i]["confidence"]["score"][0], low_indices[0]))
                high_confidence_facts = list(map(lambda i: sentence["statements"][i]["fact"], high_indices[0]))
            except:
                print("Error in Extracting Score..")

            else:
                for low_fact, low_score in zip(low_confidence_facts, low_confidence_score):  
                    print("[ORIGIN FACT]:", low_fact, low_score)

                    for _ in range(10):     
                        #try:           
                        factor_prompt = FACTORS_FORMAT.format(sentence = low_fact)
                        factor = model.generate(factor_prompt, max_tokens=128, temperature=0.0)
                        _factor = re.findall(r"\[.*?\]", factor)
                        if len(_factor)!=0:
                            factor=_factor[0]
                        else:
                            factor=factor.replace("FACTORS","").strip()
                        
                        revise_prompt = REVISE_FORMAT.format(sentence = low_fact, factor=factor.strip(), reference= "\n".join(high_confidence_facts))
                        revise = model.generate(revise_prompt, max_tokens=128, temperature=0.0)
                        print("[CORRECTIONS]:", factor,":",revise)

                        if "NoError" not in revise:
                            agg_prompt = AGG_FACT_FORMAT.format(ori_fact = low_fact, revise_fact = revise)
                            revise_fact = model.generate(agg_prompt, max_tokens=128, temperature=0.0).replace("REVISE:","").strip()
                            print("[REVISE FACT]: ",revise_fact)
                            ori_self_confidence_response = model.generate(FACT_SELF_CONF_FORMAT.format(criterion=CRITERION_CONTINUE, question=sentence["question"], twofacts=low_fact.strip()))
                            revise_self_confidence_response = model.generate(FACT_SELF_CONF_FORMAT.format(criterion=CRITERION_CONTINUE, question=sentence["question"], twofacts=revise_fact.strip()))
                            print("[CONFIDENCE]: ")
                            print(ori_self_confidence_response)
                            print(revise_self_confidence_response)
                            
                            ori_score = re.findall(r'\[\d\.\d{2}\]', ori_self_confidence_response)
                            revise_score = re.findall(r'\[\d\.\d{2}\]', revise_self_confidence_response)
                            if len(ori_score)!=0 and len(revise_score)!=0:
                                if float(revise_score[0][1:-1]) > float(ori_score[0][1:-1]):
                                    print("[INCREASE!!]: ", ori_score, "->",revise_score)
                                    sentence["revise"].append({"ori_fact":(low_fact, ori_score[0]), "factor":factor, "correction":revise, "revise_fact":(revise_fact,revise_score[0])})
                                    break
                                else:
                                    print("[NOT INCREASE]: continue..")
                            else:
                                continue
                        else:
                            print("[REVISE FACT]: No Error Skip")
                            break
                        # except:
                        #     print("Failed, Retry..")
                        #     continue
        else:
            print('confidence_vector std is 0', confidence_vector)

        
        print(sentence["revise"])
        print("====================")
        # exit(0)
        return_list.append(sentence)
        REVISE_SAVE_PATH='./results/{}_REVISE.json'.format(main_config.responder_model_short)
        with open(REVISE_SAVE_PATH, 'w') as outfile:
            json.dump(return_list, outfile)

def gpt4_eval(path):

    gpt_4 = modeling.Model(
        model_name="OPENAI:gpt-4-0125-preview",
        temperature=0.0,
        show_responses=main_config.show_responder_responses,
        show_prompts=main_config.show_responder_prompts,
        path = None,
        device = None
    )
    #print_config('GPT-4', gpt_4)

    with open(path) as f:
        revise_results = json.load(f)

    num_total = len(revise_results)

    eval_list = []
    
    num_revise = 0
    num_improve = 0
    num_same = 0
    num_regress = 0
    num_eval_fail =0

    for index, sentence in enumerate(revise_results):
        if len(sentence["revise"])>0:
            num_revise = num_revise + 1
            for i in sentence["revise"]:
                eval_prompt = GPT4_EVAL_FORMAT.format(question=sentence["question"], response=sentence["response"], all_facts="\n".join([s["fact"] for s in sentence["statements"]]), ori_fact=i["ori_fact"][0], revise_fact=i["revise_fact"][0])
                print(eval_prompt)
                
                eval_result = gpt_4.generate(eval_prompt, max_tokens=128, temperature=0.0)
                print("-----------------------------")
                print(eval_result)
                print("\n========================================\n\n\n")
                #exit(0)
                i["eval"]=eval_result

                if len(re.findall('REVISION: IMPROVED', eval_result))>0:
                    num_improve+=1
                elif len(re.findall('REVISION: SAME', eval_result))>0:
                    num_same+=1
                elif len(re.findall('REVISION: REGRESSED', eval_result))>0:
                    num_regress+=1
                else:
                    num_eval_fail+=1
        eval_list.append(sentence)
        return_dict={"eval_list":eval_list, "eval_summary":{"num_total":num_total, "num_revise":num_revise, "num_improve":num_improve, "num_same":num_same, "num_regress":num_regress, "num_eval_fail":num_eval_fail}}
        with open(path.replace(".json","")+"_EVAL.json", 'w') as outfile:
            json.dump(return_dict, outfile)
       
        

        


        


def main(_):
    # check_model_consistency(main_config.responder_model_short, result_path)

    # if main_config.responder_model in OPEN_SOURCE_TEMPLATE:
    #     path = os.path.join(main_config.path,main_config.responder_model)
    #     device = main_config.device
    # else:
    #     path = None
    #     device = None


    # responder = modeling.Model(
    #     model_name=main_config.responder_model,
    #     temperature=0.7,
    #     show_responses=main_config.show_responder_responses,
    #     show_prompts=main_config.show_responder_prompts,
    #     path = path,
    #     device = device
    # )
    # print_config('Responder', responder)

    #run(result_path, responder)
    REVISE_SAVE_PATH = './results/asqa/vicuna-13b_REVISE.json'
    gpt4_eval(REVISE_SAVE_PATH)

    


# if resume_result_path:
#     with open(resume_result_path) as f:
#         return_list=json.load(f)

#     break_point = RESUME_BREAK_POINT
#     should_begin=False

#     for index, data in enumerate(json_data):

#         if index<break_point:
#             continue
        
#         question = data["question"]

#         # if 'Arduino Uno board' in question:
#         #     print(index)
#         #     print(return_list[-1]["question"])
#         #     print('\n',question)

#         #     print(return_list[-1]["question"] == question)
#         #     exit(0)
#         # else:
#         #     continue

#         if question == return_list[-1]["question"]:
#             print("it is the last, setting should_begin=True..")
#             should_begin=True
#             break
#         else:
#             print("wrong last, should not begin\n")
#             print("question",question,'\n')
#             print("list",return_list[-1]["question"])
#             exit(0)

#     if should_begin:
#         print("start..")
#     else:
#         exit(0)
# else:
#     return_list = []



if __name__ == '__main__':
  app.run(main)

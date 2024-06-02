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

result_path = './results/gpt_35_turbo_FACT_CONF_521.json'
number_of_samples=500

model_name = result_path.split('/')[-1].replace(".json","").split('_CONF')[0]
print('model_name',model_name)

def check_model_consistency(model_name, path):
    path = path.split("/")[-1].split("b")[0]+'bo'
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
        if index <1:
            continue
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
            #try:
            mean_value = confidence_vector.mean()
            low_indices = np.where(confidence_vector < mean_value)
            high_indices = np.where(confidence_vector >= mean_value)
            #response = [sentence["statements"][i]["fact"]+":" + str(sentence["statements"][i]["confidence"]["score"][0]) for i in range(len(sentence["statements"]))]
            #low_confidence_facts = list(map(lambda i: sentence["statements"][i]["fact"]+":"+str(sentence["statements"][i]["confidence"]["score"][0]), low_indices[0]))
            #high_confidence_facts = list(map(lambda i: sentence["statements"][i]["fact"]+":"+str(sentence["statements"][i]["confidence"]["score"][0]), high_indices[0]))

            low_confidence_facts = list(map(lambda i: sentence["statements"][i]["fact"], low_indices[0]))
            low_confidence_score = list(map(lambda i: sentence["statements"][i]["confidence"]["score"][0], low_indices[0]))
            high_confidence_facts = list(map(lambda i: sentence["statements"][i]["fact"], high_indices[0]))

            # print(low_confidence_facts)
            # print(low_confidence_score)

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


            # except:
            #     print("WRONG #2!!")

        else:
            print('confidence_vector std is 0', confidence_vector)

        
        print(sentence["revise"])
        print("====================")
        # exit(0)
        return_list.append(sentence)
        with open('./results/{}_REVISE.json'.format(main_config.responder_model_short), 'w') as outfile:
            json.dump(return_list, outfile)

def main(_):
    check_model_consistency(main_config.responder_model_short, result_path)

    if main_config.responder_model in OPEN_SOURCE_TEMPLATE:
        path = os.path.join(main_config.path,main_config.responder_model)
        device = main_config.device
    else:
        path = None
        device = None


    responder = modeling.Model(
        model_name=main_config.responder_model,
        temperature=0.7,
        show_responses=main_config.show_responder_responses,
        show_prompts=main_config.show_responder_prompts,
        path = path,
        device = device
    )
    print_config('Responder', responder)

    run(result_path, responder)

    




if __name__ == '__main__':
  app.run(main)

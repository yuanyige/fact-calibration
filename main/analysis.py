import json
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re
import numpy as np 

result_path = './results/vicuna-13b_FACT_CONF.json'
result_path_base = './results/vicuna-13b_NOFACT_CONF.json'
number_of_samples=500

model_name = result_path.split('/')[-1].replace(".json","")
model_name = model_name.split('_CONF')[0]


def run(path, path_base):
    
    with open(path) as f:
        results = json.load(f)

    with open(path_base) as f:
        results_base = json.load(f)
    
    max_base_diff, mid_base_diff, mean_base_diff = [],[],[]

    all_confidence_vector = []
    all_confidence_vector_max = []
    all_confidence_vector_min = []
    all_confidence_vector_mean = []
    all_confidence_vector_mid = []
    all_confidence_vector_std = []
    all_base_confidence=[]
    

    for index, (sentence, sentence_base) in enumerate(zip(results,results_base)):
        
        if index >= number_of_samples:
            break


        sentence_correctness = 0
        sentence_confidence = 0
        confidence_vector=[]
        num_facts = 0

        try:
            for item in sentence["statements"]:
                
                correct_score = 1.0 if item["correctness"]=='Supported' else 0.0
                relevant_score = 1.0 if item["relevance"]=='Foo' else 0.0
                score2 = re.findall(r'\d\.\d{2}', item["confidence"]["response"])
                if len(item["confidence"]["score"])!=0:
                    score1 = re.findall(r'\d\.\d{2}', item["confidence"]["score"][0])
                    confident_score=float(score1[0])
                    print('fact confident_score',confident_score,item["fact"],correct_score)
                    num_facts = num_facts + 1
                elif len(score2)!=0:
                    confident_score=float(score2[0])
                    num_facts = num_facts + 1
                else:
                    print("WRONG #1!!")
                
                confidence_vector.append(float(confident_score))
                reweight_correctness = float(correct_score) *float(relevant_score)
                sentence_correctness = sentence_correctness + reweight_correctness
                sentence_confidence = sentence_confidence + float(confident_score)
            sentence_correctness = sentence_correctness / num_facts
            sentence_confidence = sentence_confidence / num_facts

            print("sentence_confidence", confidence_vector, 'mean', sentence_confidence)

            all_confidence_vector.append(confidence_vector)
            confidence_vector=np.array(confidence_vector)

            max_value = confidence_vector.max()
            min_value = confidence_vector.min()
            mean_value = confidence_vector.mean()
            mid_value = np.median(confidence_vector)
            std_value = confidence_vector.std()

            print('max-min', max_value, min_value)
            print('mean', mean_value)
            print('median', mid_value)

            all_confidence_vector_max.append(max_value)
            all_confidence_vector_min.append(min_value)
            all_confidence_vector_mean.append(mean_value)
            all_confidence_vector_mid.append(mid_value)
            all_confidence_vector_std.append(std_value)



            ###
            score2 = re.findall(r'\d\.\d{2}', sentence_base["confidence"]["response"])
            if len(sentence_base["confidence"]["score"])!=0:
                score1 = re.findall(r'\d\.\d{2}', sentence_base["confidence"]["score"][0])
                confident_score=float(score1[0])
                num_facts = num_facts + 1
            elif len(score2)!=0:
                confident_score=float(score2[0])
                num_facts = num_facts + 1
            else:
                print("WRONG #2!!")
            
            print("sentence_base", confident_score)
            all_base_confidence.append(confident_score)
            max_base_diff.append(abs(confident_score-confidence_vector.max()))
            mid_base_diff.append(abs(confident_score-np.median(confidence_vector)))
            mean_base_diff.append(abs(confident_score-confidence_vector.mean()))
                
        except:
            print(sentence)
            print("===========WRONG!!")
            continue



    # 使用Seaborn绘制箱形图
    # sns.boxplot(data=all_std)
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))  # 2行1列的子图
    violin = sns.violinplot([all_base_confidence, all_confidence_vector_mean, all_confidence_vector_mid, all_confidence_vector_max, all_confidence_vector_min], cut=0, ax=axs[0],linewidth=1)
    color=['gray','skyblue','skyblue','skyblue','skyblue']
    for i, art in enumerate(violin.collections):
        # violin.collections包含了小提琴图的各个部分，比如身体、棒子等。
        art.set_edgecolor('k')  # 设置边缘颜色
        art.set_facecolor(color[i])  # 设置填充颜色
    axs[0].set_xticklabels(['Baseline','Ours Mean','Ours Mid','Ours Max','Ours Min'])


    num_sample = 100
    sorted_indices = [index for index, _ in sorted(enumerate(all_confidence_vector), key=lambda x: np.std(x[1]), reverse=True)]
    #print("sorted_indices",sorted_indices)
    sorted_all_confidence_vector = [all_confidence_vector[i] for i in sorted_indices]
    sorted_all_base_confidence = [all_base_confidence[i] for i in sorted_indices]

    # sorted_all_confidence_vector = sorted(all_confidence_vector, key=lambda x: np.std(x),reverse=True)
    # sns.violinplot(sorted_all_confidence_vector[:num_sample], cut=0, color='skyblue', ax=axs[1], linewidth=1, bw=0.5)
    sns.boxplot(sorted_all_confidence_vector[:num_sample], color='skyblue', ax=axs[1], linewidth=1)

    print('sorted_all_base_confidence',sorted_all_base_confidence[:num_sample])
    for i, height in enumerate(sorted_all_base_confidence[:num_sample]):
        axs[1].axhline(y=height, color='red', linestyle='-', xmin=(i+0.4)/num_sample ,xmax=(i+1-0.4)/num_sample, linewidth=5.5, alpha=0.7)
    axs[1].set_xticks([])


    plt.tight_layout()
    plt.savefig("./results/box/{}_{}.pdf".format(model_name, number_of_samples), format='pdf')
    




run(result_path,result_path_base)
exit(0)


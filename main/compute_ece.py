import json
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re

result_path = './results/llama_2_7b_FACT_CONF_596.json'
# fact_aggregation = True
mode = 'fact' # factagg / fact / nofact
number_of_samples=500

bins = [(0.0, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.5),
        (0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.0)]
bin_counts = [0] * len(bins)
bin_accs = [0] * len(bins)
bin_diffs = [0] * len(bins)

CONFIDENCE_MAP={'[5/5]':0.99999,'[4/5]':0.79999,'[3/5]':0.59999,'[2/5]':0.39999,'[1/5]':0.1999,'[0/5]':0.0,}


model_name = result_path.split('/')[-1].replace(".json","")
model_name = model_name.split('_CONF')[0]
with open(result_path) as f:
    results=json.load(f)

def run_with_fact_aggregation(results):
    for index, sentence in enumerate(results):
        
        try:
            if index >= number_of_samples:
                break

            wrong_sentence=[]
            return_sentence={}

            sentence_correctness = 0
            sentence_confidence = 0
            num_facts = 0
            for item in sentence["statements"]:
                
                correct_score = 1.0 if item["correctness"]=='Supported' else 0.0
                relevant_score = 1.0 if item["relevance"]=='Foo' else 0.0
                # confidence_score_list = list(set(item["confidence"]["score"]))
                # if len(confidence_score_list)==1:
                #     confident_score = CONFIDENCE_MAP[confidence_score_list[0]]
                #     num_facts = num_facts + 1
                # elif :
                #     print("===================Oooops, ambiguous confidence")
                #     print(item["confidence"]["response"])
                #     continue
                
                # confident_score = CONFIDENCE_MAP[item["confidence"]["score"][0]]
                score2 = re.findall(r'\d\.\d{2}', item["confidence"]["response"])
                if len(item["confidence"]["score"])!=0:
                    score1 = re.findall(r'\d\.\d{2}', item["confidence"]["score"][0])
                    confident_score=float(score1[0])
                    print('fact confident_score',confident_score)
                    num_facts = num_facts + 1
                elif len(score2)!=0:
                    #print("===================score not found in CONFIDENCE, but found in EXPLANATION")
                    #print(item["confidence"]["response"])
                    confident_score=float(score2[0])
                    num_facts = num_facts + 1
                else:
                    #print("===================score totally not found")
                    #print(item["confidence"]["response"])
                    continue

                # print(correct_score,relevant_score,confident_score,num_facts)
                if confident_score!=0:
                    confident_score = confident_score-0.00001
                reweight_correctness = float(correct_score) *float(relevant_score)
                sentence_correctness = sentence_correctness + reweight_correctness
                sentence_confidence = sentence_confidence + float(confident_score)
            # print(sentence_correctness)
            # print(num_facts)
            sentence_correctness = sentence_correctness / num_facts
            sentence_confidence = sentence_confidence / num_facts


            print("index",index)
            for i, (bin_start, bin_end) in enumerate(bins):
                if bin_start <= sentence_confidence < bin_end:
                    # if confident_score == 1:
                    #     bin_counts[-1] += 1
                    bin_counts[i] += 1
                    bin_diffs[i] += abs(sentence_correctness - sentence_confidence)
                    bin_accs[i] += sentence_correctness
                    break
                
        except:
            print("===========wwrong")
            print(sentence)
            continue
            # print(sentence["statements"])
            # exit(0)

def run_without_fact_aggregation(results):
    for index, sentence in enumerate(results):
        if index >= number_of_samples:
            break
        wrong_sentence=[]
        return_sentence={}

        sentence_correctness = 0
        sentence_confidence = 0
        num_facts = 0
        for item in sentence["statements"]:
            
            correct_score = 1.0 if item["correctness"]=='Supported' else 0.0
            relevant_score = 1.0 if item["relevance"]=='Foo' else 0.0
            confidence_score_list = list(set(item["confidence"]["score"]))
            # if len(confidence_score_list)==1:
            #     confident_score = CONFIDENCE_MAP[confidence_score_list[0]]
            #     num_facts = num_facts + 1
            # else:
            #     print("Oooops, ambiguous confidence")
            #     continue

            score2 = re.findall(r'\d\.\d{2}', item["confidence"]["response"])
            if len(item["confidence"]["score"])!=0:
                score1 = re.findall(r'\d\.\d{2}', item["confidence"]["score"][0])
                confident_score=float(score1[0])
                print(confident_score)
                num_facts = num_facts + 1
            elif len(score2)!=0:
                print("===================score not found in CONFIDENCE, but found in EXPLANATION")
                print(item["confidence"]["response"])
                confident_score=float(score2[0])
                num_facts = num_facts + 1
            else:
                print("===================score totally not found")
                print(item["confidence"]["response"])
                continue

            for i, (bin_start, bin_end) in enumerate(bins):
                if bin_start <= confident_score < bin_end:

                    # if confident_score == 1:
                    #     bin_counts[-1] += 1
                    # else:
                    bin_counts[i] += 1
                    bin_diffs[i] += abs(correct_score - confident_score)
                    bin_accs[i] += correct_score
                    break

def run_no_fact(results):
    for index, sentence in enumerate(results):
        if index >= number_of_samples:
            break
        try:
            correct_score = sentence["correctness"]
            if len(sentence["confidence"]["score"])!=0:
                findall_confident_score = re.findall(r'\d\.\d{2}', sentence["confidence"]["score"][0])
                confident_score = float(findall_confident_score[0])
            else:
                findall_confident_score = re.findall(r'\d\.\d{2}', sentence["confidence"]["response"])
                confident_score = float(findall_confident_score[0])
            if confident_score!=0:
                confident_score = confident_score-0.00001
            
            for i, (bin_start, bin_end) in enumerate(bins):
                if bin_start <= confident_score < bin_end:

                    # if confident_score == 1:
                    #     bin_counts[-1] += 1
                    # else:
                    bin_counts[i] += 1
                    bin_diffs[i] += abs(correct_score - confident_score)
                    bin_accs[i] += correct_score
                    break
        except:
            print("\n===================wrong")
            print(sentence["question"])
            #print(sentence["confidence"]["response"])

if mode == 'factagg':
    run_with_fact_aggregation(results)
elif mode == 'fact':
    run_without_fact_aggregation(results)
elif mode == 'nofact':
    run_no_fact(results)

total_diff = 0
total_count = 0
for i, (count, diff, acc, range) in  enumerate(zip(bin_counts, bin_diffs, bin_accs, bins)):
    if count > 1:
        bin_ece = diff / count
        bin_acc = acc / count
        bin_accs[i] = bin_acc
        total_diff += diff
        total_count += count
        print(f"Bin {range} ECE: {bin_ece}, Acc: {bin_acc}, Samples: {count}")
    elif count ==1 :
        print("only one sample")
        bin_counts[i]=0
        bin_diffs[i]=0
        bin_accs[i]=0
    else:
        print("no sample")

# ECE
total_ece = total_diff / total_count if total_count > 0 else 0
print(f"Total Expected Calibration Error (ECE): {total_ece}")

bin_count_sum = 0
for i in bin_counts:
    bin_count_sum = bin_count_sum + i
print("Bin Count Sum:",bin_count_sum)

# Hist
def thousands_formatter(x, pos):
    return '%1.0f' % (x)

fig, ax1 = plt.subplots(figsize=(6.6, 6))
x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
# 
# x=[0.0,0.2,0.4,0.6,0.8]
ax1.bar(x, [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0], color='grey', alpha=1, width=0.1, edgecolor='white', linewidth=0.5, align='edge', label='Gap')
ax1.bar(x, bin_accs, color='#8080F5', alpha=0.3, width=0.1, edgecolor='black', linewidth=0.5, align='edge', label=model_name)

# ax1.plot(x2, [-0.05, 0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95, 1.05], color='k', linestyle='dashed', linewidth=2.5)
ax1.set_xlim([0, 1])
ax1.set_ylim([0, 1])


ax2 = ax1.twinx()
x3=[i+0.03 for i in x]
ax2.bar(x3, bin_counts, width=0.04, color='#E55050', align='edge',label="#Sample") 
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(thousands_formatter))


max_sample=(number_of_samples//3)*5
ax2.set_ylim([0,max_sample])

ax2.set_ylabel('Number of Samples', fontsize = 19)
ax1.set_xlabel("Confidence", fontsize = 19)
ax1.set_ylabel("Accuracy", fontsize = 19)


handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles = handles1 + handles2
labels = labels1 + labels2

plt.legend(handles, labels, loc="upper left", ncol=3)
pos = max_sample *0.85
plt.text(0.02, pos, r"ECE={:.2f}".format(total_ece),fontsize = 24)
#plt.text(0.02, 90, r"MCE($\downarrow$)={:.2f}%".format(mces*100),fontsize = 24, fontproperties=myfont)
#plt.title(name,fontsize = 24)


plt.tight_layout()
plt.savefig("./results/hist3/{}_{}.pdf".format(model_name, number_of_samples), format='pdf')
plt.close()

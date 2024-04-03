import json
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

result_path = './output-llama-2-7b-chat-hf-gpt-4-turbo-preview-temp0.3gpustat.json'

if result_path:
    with open(result_path) as f:
        results=json.load(f)
else:
    results = {}


bins = [(0.0, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.5),
        (0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 1.0)]
bin_counts = [0] * len(bins)
bin_accs = [0] * len(bins)
bin_diffs = [0] * len(bins)

CONFIDENCE_MAP={'5/5':1.0,}

for id_, details in results.items():
    # print(id_)
    # print(details)
    wrong_sentence=[]
    return_sentence={}
    try:
        sentence_correctness = 0
        sentence_confidence = 0
        num_facts = 0
        for item in details["split"]:
            num_facts = num_facts + 1
            # if item["correctness"]:
            correct_score = 1.0 if item["correctness"]=='Support' else 0.0
            relevant_score = 1.0 if item["relevance"]=='Foo' else 0.0
            confident_score = CONFIDENCE_MAP[item["confidence"]["scores"]]

            reweight_correctness = float(item["correctness"]) *float(item["relevance"])
            sentence_correctness = sentence_correctness + reweight_correctness
            sentence_confidence = sentence_confidence + float(item["confidence"])
        # print(sentence_correctness)
        # print(num_facts)
        sentence_correctness = sentence_correctness / num_facts
        sentence_confidence = sentence_confidence / num_facts

        for i, (bin_start, bin_end) in enumerate(bins):
            if bin_start <= sentence_confidence < bin_end:
                bin_counts[i] += 1
                bin_diffs[i] += abs(sentence_correctness - sentence_confidence)
                bin_accs[i] += sentence_correctness
                break
    except:
        wrong_sentence.append(id_)

total_diff = 0
total_count = 0
for i, (count, diff, acc, range) in  enumerate(zip(bin_counts, bin_diffs, bin_accs, bins)):
    if count > 0:
        bin_ece = diff / count
        bin_acc = acc / count
        bin_accs[i] = bin_acc
        total_diff += diff
        total_count += count
        print(f"Bin {range} ECE: {bin_ece}, Acc: {bin_acc}, Samples: {count}")

# ECE
total_ece = total_diff / total_count if total_count > 0 else 0
print(f"Total Expected Calibration Error (ECE): {total_ece}")


# Hist
def thousands_formatter(x, pos):
    return '%1.0fk' % (x * 1e-3)

fig, ax1 = plt.subplots(figsize=(6.6, 6))
x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
ax1.bar(x, [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0], color='grey', alpha=1, width=0.1, edgecolor='white', linewidth=0.5, align='edge', label='Gap')
ax1.bar(x, bin_accs, color='#8080F5', alpha=0.3, width=0.1, edgecolor='black', linewidth=0.5, align='edge', label='llama2')

# ax1.plot(x2, [-0.05, 0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95, 1.05], color='k', linestyle='dashed', linewidth=2.5)
ax1.set_xlim([0, 1])
ax1.set_ylim([0, 1])


ax2 = ax1.twinx()
x3=[i+0.03 for i in x]
ax2.bar(x3, bin_counts, width=0.04, color='#E55050', align='edge',label="#Sample") 
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(thousands_formatter))
ax2.set_ylim([0,500])

ax2.set_ylabel('Number of Samples', fontsize = 19)
ax1.set_xlabel("Confidence", fontsize = 19)
ax1.set_ylabel("Accuracy", fontsize = 19)


handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles = handles1 + handles2
labels = labels1 + labels2

plt.legend(handles, labels, loc="upper left", ncol=3)
# plt.text(0.02, 10100, r"ECE($\downarrow$)={:.2f}%".format(eces*100),fontsize = 24,fontproperties=myfont)
# plt.text(0.02, 9100, r"MCE($\downarrow$)={:.2f}%".format(mces*100),fontsize = 24, fontproperties=myfont)
# plt.title(name,fontsize = 24,fontproperties=myfont)

plt.tight_layout()
plt.savefig("./results/hist.pdf", format='pdf')
plt.close()

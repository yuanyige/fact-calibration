
SYMBOL = 'Foo'
NOT_SYMBOL = 'Not Foo'


CRITERION_CONTINUE = """\
1.00 - Completely Correct and Completely Relevant: The STATEMENT directly addresses the QUESTION with information that is both completely correct and completely relevant.
[0.80-1.00) - Mostly Correct and Relevant: The STATEMENT largely addresses the QUESTION, containing only slight inaccuracies or irrelevancies.
[0.60-0.80) - Partially Correct and Relevant: The STATEMENT is on topic and attempts to address the QUESTION, but includes some inaccuracies or irrelevancies.
[0.40-0.60) - Somewhat Incorrect and Irrelevant: The STATEMENT touches upon the topic of the QUESTION, or includes obvious inaccuracies or irrelevancies.
[0.20-0.40) - Mostly Incorrect or Irrelevant: The statement has some connection to the question but contains substantial inaccuracies or often misses the core topic.
(0.00-0.20) - Predominantly Incorrect or Irrelevant: The statement has minimal to no connection to the question and is characterized by overwhelming inaccuracies or a complete omission of the core topic.
0.00 - Completely Incorrect or Completely Irrelevant: The STATEMENT completely fails to address the QUESTION with incorrect information, or is entirely off-topic.
"""


CRITERION_DISCRETE = """\
5 - Completely Correct and Completely Relevant: The STATEMENT directly addresses the QUESTION with information that is both completely correct and completely relevant.
4 - Mostly Correct and Relevant: The STATEMENT largely addresses the QUESTION, containing only slight inaccuracies or irrelevancies.
3 - Partially Correct and Relevant: The STATEMENT is on topic and attempts to address the QUESTION, but includes some inaccuracies or irrelevancies.
2 - Somewhat Incorrect and Irrelevant: The STATEMENT merely touches upon the topic of the QUESTION, and includes obvious inaccuracies or irrelevancies.
1 - Mostly Incorrect or Irrelevant: The STATEMENT largely fails to address the QUESTION, containing significant inaccuracies or missing the main topic.
0 - Completely Incorrect or Completely Irrelevant: The STATEMENT completely fails to address the QUESTION with incorrect information, or is entirely off-topic.
"""

    
SELF_CONF_FORMAT_CONTINUE = """\  
Instructions:
1. The following STATEMENT has been extracted from the broader context of the \
given RESPONSE to the given QUESTION.
2. Indicate how confident you are in the accuracy of the STATEMENT \
when answering the QUESTION, based on your knowledge.
3. The confidence evaluation should be a value between 0 and 1 (with two decimal places retained), based on the following scoring criterion: \
{criterion}
4. Your task is to do this for the STATEMENT, RESPONSE and QUESTION under "Your Task". \
Some examples have been provided for you to learn how to do this task.



Example 1:
QUESTION:
Who is Quoc Le?

RESPONSE:
After completing his Ph.D., Quoc Le joined ByteDance, where he has been \
working on a variety of deep learning projects. Quoc is well-respected by many \
of his peers, such as Geoffrey Hinton, who is an adjunct professor at the \
University of Montreal and teaches courses on deep learning.

STATEMENT:
Quoc Le joined ByteDance.

CONFIDENCE:
[0.00]

EXPLANATION:
For correctness, Quoc Le did not join ByteDance. Therefore, this STATEMENT is [Completely Incorrect].\
For Relevance, The subject of the QUESTION is Quoc Le. The subject of the STATEMENT is \
Quoc Le. Therefore, this STATEMENT is [Completely Relevant].



Example 2:
QUESTION:
Who is Quoc Le?

RESPONSE:
After completing his Ph.D., Quoc Le joined Google Brain, where he has been \
working on a variety of deep learning projects. Messi is a football player.

STATEMENT:
Messi is a football player.

CONFIDENCE:
[0.15]

EXPLANATION:
For correctness, Messi is a football player. Therefore, this STATEMENT is [Completely Correct].\
For Relevance, The subject of the QUESTION is Quoc Le. The subject of the STATEMENT is \
Messi. Although both subjects are celebrities, they belong to completely different \
fields, namely deep learning and football. Furthermore, the response does not contain \
any phrases that explain the relationship between Quoc Le and Messi. Therefore, \
this STATEMENT is [Predominantly Irrelevant].



Example 3:
QUESTION:
Who is Quoc Le?

RESPONSE:
After completing his Ph.D., Quoc Le joined Google Brain, where he has been \
working on a variety of deep learning projects. Geoffrey Hinton is an adjunct \
professor at the University of Montreal, where he teaches courses on deep learning.

STATEMENT:
Geoffrey Hinton is at the University of Montreal.

CONFIDENCE:
[0.65]

EXPLANATION:
For correctness, Geoffrey Hinton is at the University of Montreal. Therefore, this STATEMENT is [Completely Correct].\
For Relevance, the subject of the QUESTION is Quoc Le. The subject of the STATEMENT is \
Geoffrey Hinton. While both subjects seem to be related to deep learning, \
the RESPONSE does not contain any phrases that explain what the relationship \
between Quoc Le and Geoffrey Hinton is. Therefore, the STATEMENT is [Partially Relevant].



Example 4:
QUESTION:
Who is Quoc Le?

RESPONSE:
After completing his Ph.D., Quoc Le joined Google Brain, where he has been \
working on a variety of deep learning projects. Quoc is well-respected by many \
of his peers, such as Geoffrey Hinton, who is an adjunct professor at the \
University of Montreal and teaches courses on deep learning.

STATEMENT:
Geoffrey Hinton is at the University of Montreal.

CONFIDENCE:
[1.00]

EXPLANATION:
For correctness, Geoffrey Hinton is at the University of Montreal. Therefore, this STATEMENT is [Completely Correct].\
For Relevance, the subject of the QUESTION is Quoc Le. The subject of the STATEMENT is \
Geoffrey Hinton. The phrase "Quoc is well-respected by many of his peers, such \
as Geoffrey Hinton" from the RESPONSE shows that the relationship between Quoc \
Le and Geoffrey Hinton is that they are peers. For this reason, the STATEMENT is [Completely Relevant].


Your Task:
QUESTION:
{question}

RESPONSE:
{response}

STATEMENT:
{statement}
"""


WHOLE_SELF_CONF_FORMAT_CONTINUE = """\  
Instructions:
1. The following RESPONSE is the answer to the given QUESTION. \
2. Indicate how confident you are in the accuracy of the RESPONSE \
when answering the QUESTION, based on your knowledge.
3. The confidence evaluation should be a value between 0 and 1 (with two decimal places retained), based on the following scoring criterion: \
{criterion}
4. Your task is to do this for the RESPONSE and QUESTION under "Your Task". \
Some examples have been provided for you to learn how to do this task.



Example 1:
QUESTION:
Who is Quoc Le?

RESPONSE:
Quoc Le is a research scientist. After completing his Ph.D., Quoc Le joined ByteDance, where he has been \
working on a variety of deep learning projects. Quoc is well-respected by many \
of his peers, such as Geoffrey Hinton, who is an adjunct professor at the \
University of Montreal and teaches courses on deep learning.

CONFIDENCE:
[0.35]

EXPLANATION:
For correctness, Quoc Le did not join ByteDance. Therefore, this RESPONSE is [Mostly Incorrect].\
For Relevance, The subject of the QUESTION is Quoc Le. The subject of the RESPONSE is \
Quoc Le. Therefore, this RESPONSE is [Completely Relevant].



Example 2:
QUESTION:
Who is Quoc Le?

RESPONSE:
Quoc Le is a research scientist. After completing his Ph.D., Quoc Le joined Google Brain, where he has been \
working on a variety of deep learning projects. Messi is a football player.

CONFIDENCE:
[0.65]

EXPLANATION:
For correctness, this RESPONSE is [Completely Correct].\
For Relevance, The subject of the QUESTION is Quoc Le, but the RESPONSE contains information about \
Messi. Although both subjects are celebrities, they belong to completely different \
fields, namely deep learning and football. Furthermore, the response does not contain \
any phrases that explain the relationship between Quoc Le and Messi. Therefore, \
this RESPONSE is [Partially Relevant].



Example 3:
QUESTION:
Who is Quoc Le?

RESPONSE:
Quoc Le is a research scientist. After completing his Ph.D., Quoc Le joined Google Brain, where he has been \
working on a variety of deep learning projects. Geoffrey Hinton is an adjunct \
professor at the University of Montreal, where he teaches courses on deep learning.

CONFIDENCE:
[0.83]

EXPLANATION:
For correctness, this RESPONSE is [Completely Correct].\
For Relevance, the subject of the QUESTION is Quoc Le. but the RESPONSE contains information about \
Geoffrey Hinton. While both subjects seem to be related to deep learning, \
the RESPONSE does not contain any phrases that explain what the relationship \
between Quoc Le and Geoffrey Hinton is. Therefore, the RESPONSE is [Mostly Relevant].



Example 4:
QUESTION:
Who is Quoc Le?

RESPONSE:
Quoc Le is a research scientist. After completing his Ph.D., Quoc Le joined Google Brain, where he has been \
working on a variety of deep learning projects. Quoc is well-respected by many \
of his peers, such as Geoffrey Hinton, who is an adjunct professor at the \
University of Montreal and teaches courses on deep learning.

CONFIDENCE:
[1.00]

EXPLANATION:
For correctness, this RESPONSE is [Completely Correct].\
For Relevance, the subject of the QUESTION is Quoc Le. Although the RESPONSE contains information about \
Geoffrey Hinton. The phrase "Quoc is well-respected by many of his peers, such \
as Geoffrey Hinton" from the RESPONSE shows that the relationship between Quoc \
Le and Geoffrey Hinton is that they are peers. For this reason, the STATEMENT is [Completely Relevant].


Your Task:
QUESTION:
{question}

RESPONSE:
{response}
"""


    
SELF_CONF_FORMAT_DISCRETE = """\  
Instructions:
1. The following STATEMENT has been extracted from the broader context of the \
given RESPONSE to the given QUESTION.
2. Indicate how confident you are in the accuracy of the STATEMENT \
when answering the QUESTION, based on your knowledge.
3. The confidence evaluation should be based on the following scoring criterion: \
{criterion}
4. Your task is to do this for the STATEMENT, RESPONSE and QUESTION under "Your Task". \
Some examples have been provided for you to learn how to do this task.



Example 1:
QUESTION:
Who is Quoc Le?

RESPONSE:
After completing his Ph.D., Quoc Le joined ByteDance, where he has been \
working on a variety of deep learning projects. Quoc is well-respected by many \
of his peers, such as Geoffrey Hinton, who is an adjunct professor at the \
University of Montreal and teaches courses on deep learning.

STATEMENT:
Quoc Le joined ByteDance.

CONFIDENCE:
[0/5]

EXPLANATION:
For correctness, Quoc Le did not join ByteDance. Therefore, this STATEMENT is [Completely Incorrect].\
For Relevance, The subject of the QUESTION is Quoc Le. The subject of the STATEMENT is \
Quoc Le. Therefore, this STATEMENT is [Completely Relevant].



Example 2:
QUESTION:
Who is Quoc Le?

RESPONSE:
After completing his Ph.D., Quoc Le joined Google Brain, where he has been \
working on a variety of deep learning projects. Messi is a football player.

STATEMENT:
Messi is a football player.

CONFIDENCE:
[1/5]

EXPLANATION:
For correctness, Messi is a football player. Therefore, this STATEMENT is [Completely Correct].\
For Relevance, The subject of the QUESTION is Quoc Le. The subject of the STATEMENT is \
Messi. Although both subjects are celebrities, they belong to completely different \
fields, namely deep learning and football. Furthermore, the response does not contain \
any phrases that explain the relationship between Quoc Le and Messi. Therefore, \
this STATEMENT is [Mostly Irrelevant].



Example 3:
QUESTION:
Who is Quoc Le?

RESPONSE:
After completing his Ph.D., Quoc Le joined Google Brain, where he has been \
working on a variety of deep learning projects. Geoffrey Hinton is an adjunct \
professor at the University of Montreal, where he teaches courses on deep learning.

STATEMENT:
Geoffrey Hinton is at the University of Montreal.

CONFIDENCE:
[3/5]

EXPLANATION:
For correctness, Geoffrey Hinton is at the University of Montreal. Therefore, this STATEMENT is [Completely Correct].\
For Relevance, the subject of the QUESTION is Quoc Le. The subject of the STATEMENT is \
Geoffrey Hinton. While both subjects seem to be related to deep learning, \
the RESPONSE does not contain any phrases that explain what the relationship \
between Quoc Le and Geoffrey Hinton is. Therefore, the STATEMENT is [Partially Relevant].



Example 4:
QUESTION:
Who is Quoc Le?

RESPONSE:
After completing his Ph.D., Quoc Le joined Google Brain, where he has been \
working on a variety of deep learning projects. Quoc is well-respected by many \
of his peers, such as Geoffrey Hinton, who is an adjunct professor at the \
University of Montreal and teaches courses on deep learning.

STATEMENT:
Geoffrey Hinton is at the University of Montreal.

CONFIDENCE:
[5/5]

EXPLANATION:
For correctness, Geoffrey Hinton is at the University of Montreal. Therefore, this STATEMENT is [Completely Correct].\
For Relevance, the subject of the QUESTION is Quoc Le. The subject of the STATEMENT is \
Geoffrey Hinton. The phrase "Quoc is well-respected by many of his peers, such \
as Geoffrey Hinton" from the RESPONSE shows that the relationship between Quoc \
Le and Geoffrey Hinton is that they are peers. For this reason, the STATEMENT is [Completely Relevant].


Your Task:
QUESTION:
{question}

RESPONSE:
{response}

STATEMENT:
{statement}
"""




FACTORS_FORMAT='''
You are to read a sentence and identify the key factors within it. 
The task involves pinpointing the essential elements or aspects that significantly influence or characterize the situation, event, or subject described.
Return the identified key factors using the format "[factor1, factor2, ...]"


Example 1:

SENTENCE:
Quoc Le joined ByteDance to lead its AI research team.

FACTORS:
[Quoc Le, ByteDance, lead its AI research team]



Example 2:

SENTENCE:
A severe drought has led to widespread crop failure.

FACTORS:
[drought, crop failure]


Example 3:

SENTENCE:
The museum is open on Sundays due to high public demand.

FACTORS:
[The museum, open, Sundays, high public demand]


Your Task:

SENTENCE:
{sentence}
'''


REVISE_FORMAT='''
You have been provided with a sentence and some reference knowledge. \
The sentence has been analyzed, and its factors have been identified. \
However, it is acknowledged that there may be errors or inaccuracies in the identified factors.\
Your task is to first review the identified factors and check for any errors or inaccuracies. \
If there are no errors, simply return "NoError" to indicate that no corrections are needed. \
If errors are present, proceed to make the necessary corrections.
Corrections Instructions:
1. Ensure that the corrections are limited to the existing factors without adding new content.
2. Use the format "old factor -> new factor" for each correction.


Example 1:

SENTENCE:
Quoc Le joined Google to lead its AI research team.

FACTORS:
[Quoc Le, Google, lead its AI research team]

REFERENCE:
Quoc Le completed his Ph.D.
Quoc Le worked on a variety of deep learning projects

REVISE:
NoError


Example 2:

SENTENCE
Fei-Fei Li is a female historian

FACTORS:
[Fei-Fei Li, a female historian]

REFERENCE:
Fei-Fei Li's research interests include deep learning.
Fei-Fei Li's representative work is ImageNet.

REVISE:
a female historian -> a female scientist.


Your Task:

SENTENCE:
{sentence}

FACTORS:
{factor}

REFERENCE:
{reference}
'''




AGG_FACT_FORMAT='''
You will be given a SENTENCE along with its suggested CORRECTION. 
Your task is to apply the CORRECTION to the SENTENCE as indicated and return the modified sentence under REVISE.


Example 1:

SENTENCE:
Fei-Fei Li is a female historian.

CORRECTION:
a female historian -> a female scientist.

REVISE:
Fei-Fei Li is a female scientist.


Example 2:

SENTENCE
Quoc Le joined ByteDance to lead its AI research team.

CORRECTION:
ByteDance -> Google

REVISE:
Quoc Le joined Google to lead its AI research team.


Your Task:

SENTENCE:
{ori_fact}

CORRECTION:
{revise_fact}
'''

FACT_SELF_CONF_FORMAT = """\  
Instructions:
You will be given a QUESTION and a related STATEMENT.
1. Indicate how confident you are in the accuracy of the STATEMENT when answering the QUESTION, based on your knowledge.
2. The confidence evaluation should be a value between 0 and 1 (with two decimal places retained), based on the following scoring criterion: {criterion}
3. Your task is to do this for the STATEMENT and QUESTION under "Your Task". \
Some examples have been provided for you to learn how to do this task.


Example 1:
QUESTION:
Who is Quoc Le?

STATEMENT:
Quoc Le joined ByteDance.

CONFIDENCE:
Quoc Le joined ByteDance. [0.00]


Example 2:
QUESTION:
Who is Quoc Le?

STATEMENT:
Messi is a firend of Quoc Le.

CONFIDENCE:
Messi is a firend of Quoc Le. [0.65]


Your Task:
QUESTION:
{question}

STATEMENT:
{twofacts}
"""


GPT4_EVAL_FORMAT="""
You will be provided with a QUESTION, its RESPONSE, and all facts extracted from the RESPONSE under the heading "ALL FACTS".

You will also be provided with a specific fact under the heading "TARGET FACT 1", which is included in ALL FACTS. 
Additionally, you will be given a modified version of this target fact under the heading "TARGET FACT 2".
Based on your knowledge, evaluate whether the modification of the target fact is an improvement, the same, or a regression.

An improvement implies:
1. More accurate information,
2. Greater relevance to the question,
3. Minimal overlap with other facts in ALL FACTS.

A regression implies:
1. Introduction of erroneous or inaccurate information,
2. Lower relevance to the question,
3. Repetition or introduction of information that is already provided with other facts in ALL FACTS.

Special attention should be paid to ensuring that a good modification does not overly repeat or directly copy information from other facts in ALL FACTS.

QUESTION:
{question}

RESPONSE:
{response}

ALL FACTS:
{all_facts}

TARGET FACT 1:
{ori_fact}

TARGET FACT 2:
{revise_fact}

First, provide a one-sentence comparison of the two facts and explain whether you think the modification is an improvement, the same, or a regression.
Second, on a new line, state only "IMPROVED", "SAME", or "REGRESSED" to indicate the effectiveness of the modification. Your response should use the following format:

COMPARISON:
<one-sentence comparison and explanation>

REVISION: <"IMPROVED", "SAME", or "REGRESSED">
"""


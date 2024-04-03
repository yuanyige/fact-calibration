
SYMBOL = 'Foo'
NOT_SYMBOL = 'Not Foo'


CRITERION = """\
5 - Completely Correct and Completely Relevant: The STATEMENT directly addresses the QUESTION with information that is both completely correct and completely relevant.
4 - Mostly Correct and Relevant: The STATEMENT largely addresses the QUESTION, containing only slight inaccuracies or irrelevancies.
3 - Partially Correct and Relevant: The STATEMENT is on topic and attempts to address the QUESTION, but includes some inaccuracies or irrelevancies.
2 - Somewhat Incorrect and Irrelevant: The STATEMENT merely touches upon the topic of the QUESTION, and includes obvious inaccuracies or irrelevancies.
1 - Mostly Incorrect or Irrelevant: The STATEMENT largely fails to address the QUESTION, containing significant inaccuracies or missing the main topic.
0 - Completely Incorrect or Completely Irrelevant: The STATEMENT completely fails to address the QUESTION with incorrect information, or is entirely off-topic.
"""

# def confidence_prompt(question, response, statement):
    
SELF_CONF_FORMAT = """\  
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
any phrases that explain the relationship between Quoc Le and Geoffrey Hinton. Therefore, \
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


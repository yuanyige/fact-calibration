# TEMPLATE_LLAMA2_CHAT = '''<s>[INST] {task_instruction} [/INST]'''

# # TEMPLATE_LLAMA2_CHAT

OPEN_SOURCE_TEMPLATE={
    'Llama-2-7b-chat-hf':'llama-2-chat', 
    'Llama-2-13b-chat-hf':'llama-2-chat', 
    'Llama-2-70b-chat-hf':'llama-2-chat', 
    'vicuna-7b-v1.5':'vicuna',
    'vicuna-13b-v1.5':'vicuna',
    'Mistral-7B-Instruct-v0.2': 'mistral-instruct',
}

def split_response(model_name, response, prompt=None):
    if OPEN_SOURCE_TEMPLATE[model_name] == 'vicuna':
        return response.replace('</s>',"").replace('<s>',"").replace(prompt.replace('</s>',"").replace('<s>',""),"").strip()
    else:
        return response.split("[/INST]")[-1].strip().split('</s>')[0]
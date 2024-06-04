# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Shared configuration across all project code."""

import os


################################################################################
#                         FORCED SETTINGS, DO NOT EDIT
# prompt_postamble: str = The postamble to seek more details in output.
# openai_api_key: str = OpenAI API key.
# anthropic_api_key: str = Anthropic API key.
# serper_api_key: str = Serper API key.
# random_seed: int = random seed to use across codebase.
# model_options: Dict[str, str] = mapping from short model name to full name.
# model_string: Dict[str, str] = mapping from short model name to saveable name.
# task_options: Dict[str, Any] = mapping from short task name to task details.
# root_dir: str = path to folder containing all files for this project.
# path_to_data: str = directory storing task information.
# path_to_result: str = directory to output results.
################################################################################
prompt_postamble = """\
Provide as many specific details and examples as possible (such as names of \
people, numbers, events, locations, dates, times, etc.)
"""
#openai_api_key = 'sk-Jx2ofLvAjiwJ7424520b16E4E1D543Df96D448F0243c5376' #3.5
openai_api_key = 'sk-tik3GorMTLN8wjA76b70EbEe88Ba481eBc1cFc4e00Fd063c' #4
anthropic_api_key = ''
serper_api_key = 'e5b6022e29be2b57b677ab842b228ced17aca7f7'
random_seed = 1
model_options = {
    'gpt_4_turbo': 'OPENAI:gpt-4-0125-preview',
    'gpt_4': 'OPENAI:gpt-4-0613',
    'gpt_4_32k': 'OPENAI:gpt-4-32k-0613',
    'gpt_35_turbo': 'OPENAI:gpt-3.5-turbo-0125',
    'gpt_35_turbo_16k': 'OPENAI:gpt-3.5-turbo-16k-0613',
    'claude_3_opus': 'ANTHROPIC:claude-3-opus-20240229',
    'claude_3_sonnet': 'ANTHROPIC:claude-3-sonnet-20240229',
    'claude_3_haiku': 'ANTHROPIC:claude-3-haiku-20240307',
    'claude_21': 'ANTHROPIC:claude-2.1',
    'claude_20': 'ANTHROPIC:claude-2.0',
    'claude_instant': 'ANTHROPIC:claude-instant-1.2',
    'llama_2_7b': 'Llama-2-7b-chat-hf',
    'llama_2_13b': 'Llama-2-13b-chat-hf',
    'llama_2_70b': 'Llama-2-70b-chat-hf',
    'vicuna-7b':  'vicuna-7b-v1.5',
    'vicuna-13b': 'vicuna-13b-v1.5',
    'mistral-7b': 'Mistral-7B-Instruct-v0.2',
    'longchat-7b': 'longchat-7b-v1.5-32k',
}

model_string = {
    'gpt_4_turbo': 'gpt4turbo',
    'gpt_4': 'gpt4',
    'gpt_4_32k': 'gpt432k',
    'gpt_35_turbo': 'gpt35turbo',
    'gpt_35_turbo_16k': 'gpt35turbo16k',
    'claude_3_opus': 'claude3opus',
    'claude_3_sonnet': 'claude3sonnet',
    'claude_21': 'claude21',
    'claude_20': 'claude20',
    'claude_instant': 'claudeinstant',
}
task_options = {}
root_dir = '/'.join(os.path.abspath(__file__).split('/')[:-2])
path_to_data = 'datasets/'
path_to_result = 'results/'

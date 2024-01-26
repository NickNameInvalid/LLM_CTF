# pip install openai

import json
from openai import OpenAI

# read the key file
with open('./keys/mixtral_api.txt', 'r') as f_k:
    key = f_k.read()

client = OpenAI(
    api_key="EMPTY",
    base_url=key
)

# read the prompt file
with open("./experiments/prompts_open/rev/rebug1.txt", 'r') as f_p:
    prompt = f_p.read()

print("Prompt:", prompt)
print("=====================================")
print("Mixtral answer:")
resp = client.chat.completions.create(
    model='mistralai/Mixtral-8x7B-Instruct-v0.1',
    messages=[{"role": "user", "content": prompt}],
)
print(resp.choices[0].message.content)
# Can also dump the response as JSON
print()
print("JSON:")
print(resp.model_dump_json(indent=4))
print()

# # If you want to watch the response come in 
# print(">>>>>>>>>> Streaming Mode <<<<<<<<<<")
# print("Prompt:", prompt)
# print("=====================================")
# print("Mixtral answer:")
# chunks = []
# for resp in client.chat.completions.create(
#     model='mistralai/Mixtral-8x7B-Instruct-v0.1',
#     messages=[{"role": "user", "content": prompt}],
#     stream=True):
#     chunks.append(resp)
#     text = resp.choices[0].delta.content
#     if text is not None: print(text, end='', flush=True)
# print()
# print("JSON:")
# print(json.dumps([c.model_dump() for c in chunks], indent=4))

from transformers import AutoTokenizer
import transformers
import torch

model = "mistralai/Mixtral-8x7B-v0.1"

tokenizer = AutoTokenizer.from_pretrained(model)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)

prompt = open('./questions/whataxor.txt', 'r').read()
# prompt = "Write a hello world function in python.\n"
sequences = pipeline(
    prompt,
    do_sample=True,
    top_k=10,
    temperature=0.1,
    top_p=0.95,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.eos_token_id,
    max_new_tokens=300,
)
for seq in sequences:
    print(f"Result: {seq['generated_text'][len(prompt):]}")

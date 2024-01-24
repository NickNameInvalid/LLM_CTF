from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

model_name = "mistralai/Mixtral-8x7B-v0.1"
model_name = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# Need to convert the prompt to alpaca instruction format because the model is instruction-tuned
def alpaca_prompt(input):
    INSTRUCTION = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.


### Instruction:
{input}

### Response:"""
    return INSTRUCTION



def main():
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        load_in_8bit=False,
        torch_dtype=torch.float16,
        device_map="auto")
    model.eval()
    
    pass_at = 1
    prompt_file = './prompts_open/rev/baby\'s_third.txt'
    prompt = open(prompt_file, 'r').read()
    while prompt != "":
        prompt = prompt.replace('    ', '\t')
        prompt = alpaca_prompt(prompt)
        prompt_ids = tokenizer.batch_encode_plus([prompt]*max(pass_at,1), return_tensors="pt", truncation=True, max_length=2048).to(torch.cuda.current_device())
                
        max_new_tokens = 1024
        with torch.no_grad():
            answer_ids = model.generate(
                **prompt_ids,
                use_cache = True,
                pad_token_id = tokenizer.eos_token_id,
                eos_token_id = tokenizer.eos_token_id,
                max_new_tokens = max_new_tokens,
                do_sample = True,
                top_k = 0,
                top_p = 0.95,
                temperature = 0.8,
                num_beams = 1
            )
        answer_ids_trimmed = answer_ids[:, len(prompt_ids['input_ids'][0]):]
        answer_text_trimmed = tokenizer.batch_decode(answer_ids_trimmed, skip_special_tokens=True)
        answer_text = tokenizer.batch_decode(answer_ids, skip_special_tokens=True)
        torch.cuda.empty_cache()
        for answer in answer_text_trimmed:
            print(f"{answer}")
        print(f"\n\nAbove is the trimmed answer for {prompt_file}. Are you satisfied with the answer? If not, Please enter new prompt or the prompt .txt file address:")
        given_input = input()
        if given_input.endswith(".txt"):
            prompt = open(given_input, 'r').read()
        else:
            prompt = given_input


if __name__=="__main__":
    main()

from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import StoppingCriteria, StoppingCriteriaList
from transformers import LogitsProcessor, LogitsProcessorList
import transformers
import torch

model_name = "WizardLM/WizardCoder-Python-7B-V1.0"

stop_words = ["\n#", "\n```\n"]
stop_words_ids = [[13,29937], [13,28956,13], [13,28956,30004]]

def alpaca_prompt(input):
    INSTRUCTION = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.


### Instruction:
{input}

### Response:"""
    return INSTRUCTION



def main():
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        "text-generation",
        model=checkpoint,
        load_in_8bit=False,
        torch_dtype=torch.float16,
        device_map="auto")
    model.eval()

    class StopSequences(LogitsProcessor):
        def __init__(self, stop_ids, batch_size, encounters=1, eos_token_id=2):
            StoppingCriteria.__init__(self)
            self.stop_sequences = stop_ids
            self.batch_size = batch_size
            self.encounters = [encounters] * batch_size
            self.NUM_ENCOUNTERS = encounters
            self.eos_token_id = eos_token_id

        def __call__(self, input_ids, scores):
            forced_eos = torch.full((scores.size(1),), -float("inf"))
            forced_eos[self.eos_token_id] = 0
            for stop in self.stop_sequences:
                # Check if the input_ids end with the stop sequence
                for i in range(self.batch_size):
                    if self.encounters[i] <= 0:
                        continue
                    if input_ids[i][-len(stop):].tolist() == stop:
                        self.encounters[i] -= 1
                        if self.encounters[i] <= 0:
                            scores[i] = forced_eos
            return scores
    logits_processor = LogitsProcessorList([StopSequences(stop_words_ids, batch_size=max(pass_at,1), encounters=1)])

    prompt = open('whataxor.txt', 'r').read()
    while prompt != "":
        prompt = prompt.replace('    ', '\t')
        prompt = alpaca_prompt(prompt)
        prompt_ids = tokenizer.batch_encode_plus([prompt]*max(pass_at,1), return_tensors="pt", truncation=True, max_length=2048).to(torch.cuda.current_device())
                
        max_new_tokens = 256
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
                num_beams = 1,
                logits_processor = logits_processor
            )
        answer_ids = answer_ids[:, len(prompt_ids['input_ids'][0]):]
        answer_text = tokenizer.batch_decode(answer_ids, skip_special_tokens=True)
        torch.cuda.empty_cache()
        for answer in answer_text:
            print(f"{answer}")
        print(f"\n\nAre you satisfied with the answer? If not, Please enter new prompt:")
        prompt = input()


if __name__=="__main__":
    main()

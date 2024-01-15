from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import StoppingCriteria, StoppingCriteriaList
from transformers import LogitsProcessor, LogitsProcessorList
import transformers
import torch

model = "codellama/CodeLlama-7b-hf"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    load_in_8bit=False,
    torch_dtype=torch.float16,
    device_map="auto",
)

# Stopping criteria for generation using the LogitsProcessor class
class StopSequences(LogitsProcessor):
    def __init__(self, stop_ids, batch_size, encounters=1, eos_token_id=tokenizer.eos_token_id):
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

new_prompt = "Initialized"
prompt = 'import socket\n\ndef ping_exponential_backoff(host: str):'
while prompt not in ["", "exit"]:
    sequences = pipeline(
        prompt,
        do_sample=True,
        temperature=0.3,
        top_p=0.95,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
        max_length=500,
    )
    for seq in sequences:
        print(f"- {seq['generated_text']}\n\nNow please put another prompt, directly press enter to exit")
    new_prompt = input()
    prompt += new_prompt

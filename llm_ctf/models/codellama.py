from transformers import AutoTokenizer
import transformers
from .promp_temp import *
import torch

class CodeLlama:
    def __init__(self, model_name="CodeLlama-7b-hf", top_k=10, temperature=0.1, top_p=0.95, num_return_sequence=1, max_length=200) -> None:
        self.model = "codellama/" + model_name
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.model,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.sys = ""
        self.prompts = []
        self.response = []
        self.prompt_str = ""
        
        self.top_k = top_k
        self.temperature = temperature
        self.top_p = top_p
        self.num_return_sequence = num_return_sequence
        self.max_length = max_length
    
    def generate(self, prompt) -> str:
        self.append_prompts(prompt, type="user")
        sequences = self.pipeline(
        self.prompt_str,
        do_sample=True,
        top_k=self.top_k,
        temperature=self.temperature,
        top_p=self.top_p,
        num_return_sequences=self.num_return_sequence,
        eos_token_id=self.tokenizer.eos_token_id,
        max_length=self.max_length,
        )
        response = "".join([seq["generated_text"] for seq in sequences])
        self.append_prompts(response, "answer")
        return response
    
    def append_prompts(self, prompt: str, type: str) -> str:
        self.prompts += llama_template(prompt, type)
    
    def format_prompts(self) -> str:
        raise NotImplementedError
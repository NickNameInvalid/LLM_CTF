from openai import OpenAI
from ..models.base_model import BaseModel

class Mixtral8x7B(BaseModel):
    def __init__(self, model_id: str, url_path):
        super().__init__(model_id, url_path, None)
        self.url = url_path
        self.client = OpenAI(
            api_key=self.key,
            base_url=self.url
        )
        self.prompts = []
        
    def generate(self, prompt, use_file=True, temperature=1.0, top_p=1.0):
        if use_file:
            with open(prompt, 'r') as f:
                prompt = f.read()
    
        self.prompts.append({"role": "user", "content": prompt})
        resp = self.client.chat.completions.create(
            model=self.model_id,
            messages=self.prompts,
            temperature=temperature,
            top_p=top_p,
        )
        self.prompts.append({"role": "assistant", "content": resp.choices[0].message.content})
        return resp.choices[0].message.content
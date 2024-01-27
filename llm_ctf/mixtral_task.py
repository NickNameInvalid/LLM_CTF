import re
import os
from .models.mixtral import Mixtral8x7B

class MixtralTask:
    def __init__(self) -> None:
        self.task_name=""
    
    def evaluate_result():
        pass
        

def extract_python_code(text):
    pattern = r'```python\n(.*?)```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return "Python code block not found."

def mixtral_init(url_path):
    with open(url_path, 'r') as f:
        url = f.read()
    
    model = Mixtral8x7B(
        model_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        url_path=url
    )
    return model

def task_prompt(model, prompt, use_file=True):
    return model.generate(prompt, use_file=True)

def save_code(resp_text: str, save_path: str, file_name="sol.py"):
    code_snpt = extract_python_code(resp_text)
    with open(os.path.join(save_path, file_name), 'w') as f:
        f.write(code_snpt)
import re
import os
import subprocess
from .models.mixtral import Mixtral8x7B

class MixtralTask:
    def __init__(self, question_path: str, task_name: str, url_path: str) -> None:
        self.task_name= task_name
        self.question_path = question_path
        self.model = self.mixtral_init(url_path)
        self.valid = False
        
    def mixtral_init(self, url_path):
        with open(url_path, 'r') as f:
            url = f.read()
        
        model = Mixtral8x7B(
            model_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
            url_path=url
        )
        return model
    
    def extract_python_code(self, text):
        pattern = r'```python\n(.*?)```'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return "Python code block not found."
        
    def task_prompt(self, prompt, use_file=True):
        return self.model.generate(prompt, use_file=True)
    
    def save_code(self, resp_text: str, save_path: str, file_name="sol.py"):
        code_snpt = self.extract_python_code(resp_text)
        with open(os.path.join(save_path, file_name), 'w') as f:
            f.write(code_snpt)
    
    def validate_sol(self, resp: str):
        with open(os.path.join(self.question_path, 'flag.txt'), 'r') as f:
            flag = f.read().split()
        
        if flag in resp:
            print(f"Validation succeeded with returned flag {flag}")
            self.valid = True
            return self.valid
        
        p = subprocess.Popen('python ' + os.path.join(self.question_path, 'sol.py'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        res = '\n'.join(p.stdout.readlines())
        if flag in res:
            print(f"Validation succeeded with returned flag {flag}")
            self.valid = True
            return self.valid

        print(f"Validation failed, the answer returned is: \n {res}")
        return self.valid
        







        

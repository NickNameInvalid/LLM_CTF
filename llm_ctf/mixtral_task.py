import re
import os
import subprocess
from .models.mixtral import Mixtral8x7B

class MixtralTask:
    def __init__(self, question_path: str, task_config: dict, url_path: str) -> None:
        self.config = task_config
        self.chal_name = self.config["name"]
        self.chal_path = os.path.abspath(question_path)
        self.model = self.mixtral_init(url_path)
        self.valid = False
        self.real_flag = self.config["flag"] if isinstance(self.config["flag"], str) else self.config['flag']['content']
        self.challenge_container = self.challenge.get("container_image")
        self.decomp_file = self.config.get("decomp_file", None)
        self.chal_category = self.config.get("category", "tmp")
        self.sol_path = os.path.join(os.path.splitdrive(question_path)[0], "solutions", self.chal_category, self.chal_name)
        if not os.path.exists(self.sol_path):
            os.makedirs(self.sol_path)

    def _clean_sol():
        

    def init_task():
        
    
    def decomp_program():
        
        
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
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            # 返回最后一个匹配项
            return matches[-1].strip()
        else:
            return "Python code block not found."
        
    def task_prompt(self, prompt, use_file=True):
        return self.model.generate(prompt, use_file=True)
    
    def save_code(self, resp_text: str, file_name="sol.py"):
        code_snpt = self.extract_python_code(resp_text)
        with open(os.path.join(self.sol_path, file_name), 'w') as f:
            f.write(code_snpt)
    
    def validate_sol(self, resp: str):

        print("============================== CHECKING SOLUTION ==============================")
        if self.real_flag in resp:
            print(f"Validation succeeded with returned flag {self.real_flag} in answer")
            self.valid = True
            return self.valid
        # print("============================== CHECKING FLAG IN SOLVER.PY ==============================")
        p = subprocess.run(['python', os.path.join(self.chal_path, 'sol.py')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        res: str = str('\n' + p.stdout.decode("utf-8"))
        if self.real_flag in res:
            print(f"Validation succeeded with returned flag {self.real_flag} by solver")
            self.valid = True
            return self.valid

        print(f"Validation failed, the result of code execution returned is: \n {res}")
        return self.valid

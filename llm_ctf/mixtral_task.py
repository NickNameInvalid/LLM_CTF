import re
import os
import shutil
import subprocess
import stat
from .utils.ctflogging import Status
from .utils.ghidra_call import Ghidra_Call
from .utils.dockertool import DockerHelper
from .models.mixtral import Mixtral8x7B
from .prompt import *
import logging

class MixtralTask:
    def __init__(self, question_path: str, task_config: dict, url_path: str) -> None:
        self.log = Status()
        self.config = task_config
        self.chal_name = self.config["name"]
        self.chal_path = os.path.abspath(question_path)
        self.model = self.mixtral_init(url_path)
        self.valid = False
        self.real_flag = self.config["flag"] if isinstance(self.config["flag"], str) else self.config['flag']['content']
        self.challenge_container = self.config.get("container_image", None)
        self.decomp_file = self.config.get("decomp_file", None)
        self.chal_category = self.config.get("category", "tmp")
        self.sol_path = os.path.join("./solutions", self.chal_category, self.chal_name)
        self.files = self.config["files"]
        self.description = self.config.get("description", "No description provided by this challenge.")
        if not os.path.exists(self.sol_path):
            os.makedirs(self.sol_path)
        self.init_task()
        if self.decomp_file:
            self.ghidra = Ghidra_Call(self.sol_path, self.decomp_file)
            self.decomp()
        self.extra_info = []
        self.read_dir()
        self.docker_container = self.config.get("container_image", None)
        self.player_docker = "ctfenv"
        self.docker_tool = DockerHelper(self.player_docker)
        
    def read_dir(self):
        for i in self.files:
            with open(os.path.join(self.sol_path, i), "r") as f:
                try:
                    self.extra_info.append(i + ":\n" + f.read())
                except Exception as e:
                    continue
        if self.decomp_file:
            self.extra_info.append(self.ghidra._read_dump()["decomp"])
    
    def _clean_sol(self):
        if os.path.exists(self.sol_path):
            shutil.rmtree(self.sol_path)     
            
    def decomp(self):
        print(self.log.assistant_message(f"Binary file {self.decomp_file} found, do reverse engineering..."))
        self.ghidra.run_ghidra()
        
    def init_task(self):
        print(self.log.assistant_message("Init solution folder..."))
        self._clean_sol()
        # shutil.copytree(self.chal_path, self.sol_path)
        shutil.copytree(self.chal_path, self.sol_path, copy_function=shutil.copy2)
         
    def mixtral_init(self, url_path):
        with open(url_path, 'r') as f:
            url = f.read()
        
        model = Mixtral8x7B(
            model_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
            url_path=url
        )
        return model
    
    def extract_python_code(self, text):
        print(self.log.assistant_message("Format solver"))
        pattern = r'```python\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return matches[0].strip()
        else:
            return "Python code block not found."
        
    def task_prompt(self, prompt, use_file=False, append_msg="", template_prompt=True):
        if use_file:
            with open(prompt, 'r') as f:
                prompt = f.read()
                
        if template_prompt:
            prompt = PROMPT_INIT.format(category=self.chal_category, category_description=category_friendly[self.chal_category], 
                                        name=self.chal_name, files=",".join(self.files), description=self.description)
        print(self.log.user_message(prompt + '\n' + "\n".join(self.extra_info) + append_msg))
        resp = self.model.generate(prompt + "\n".join(self.extra_info), append_msg=append_msg)
        print(self.log.assistant_message(resp))
        return resp
    
    def save_code(self, resp_text: str, file_name="sol.py"):
        code_snpt = self.extract_python_code(resp_text)
        with open(os.path.join(self.sol_path, file_name), 'w') as f:
            f.write(code_snpt)
    
    def validate_sol(self, resp: str):

        print(self.log.assistant_message(f"Checking solution..."))
        # print("============================== CHECKING SOLUTION ==============================")
        if self.real_flag in resp:
            print(f"Validation succeeded with returned flag {self.real_flag} in answer")
            self.valid = True
            return self.valid
        # print("============================== CHECKING FLAG IN SOLVER.PY ==============================")
        # os.chdir(self.sol_path)
        # subprocess.run(['chmod', "777", self.sol_path + "/*"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=5)
        try:
            p = self.docker_tool.docker_exec("python sol.py", f"/opt/exp/solutions/{self.chal_category}/\"{self.chal_name}\"")
            # p = subprocess.run(['python', "sol.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=5)
            res: str = str('\n' + p.stdout.decode("utf-8"))
        except Exception as e:
            print(f"Validation failed, solver cannot be executed or solver execution error, message shown below:")
            print(e)
            return self.valid
            
        if self.real_flag in res:
            print(f"Validation succeeded with returned flag {self.real_flag} by solver")
            self.valid = True
            return self.valid
        print(f"Validation failed, the result of code execution returned is: \n {res}")
        return self.valid

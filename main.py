import llm_ctf.mixtral_task as mixtral
import sys
import os
import json
from pathlib import Path
import subprocess

EXPERIMENT_REPEAT = 1
DEFAULT_PATH = Path(__file__).parent.resolve()

def main(question_path, prompt_path, chal_config):
    
    os.chdir(DEFAULT_PATH)
    
    mixtral_task = mixtral.MixtralTask(question_path=question_path, 
                                       task_config=chal_config,
                                       url_path=os.path.abspath("./keys/mixtral_api.txt"))
    
    resp = mixtral_task.task_prompt(prompt=prompt_path, use_file=False, append_msg="", template_prompt=True)
    # print("============================== RESPONSE FROM MODEL ==============================")
    # print(resp)
    mixtral_task.save_code(resp)
    solved = mixtral_task.validate_sol(resp)
    return solved
    
if __name__ == "__main__":
    # p = subprocess.run("sudo docker run --rm -it -v $PWD:/opt/exp ctfenv /bin/bash -c \'cd /opt/exp/solutions/rev/\"Rebug 1\"&&python sol.py\'", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=5, shell=True)

    # print(str('\n' + p.stdout.decode("utf-8")))
    if len(sys.argv) != 3:
        print("Usage: python script.py <question_path> <prompt_path>")
        sys.exit(1)
        
    question_path = str(sys.argv[1])
    prompt_path = str(sys.argv[2])
    with open(os.path.join(question_path, "challenge.json"), 'r') as f:
        chal_json = json.load(f)
        
    success = 0
    chal_name = chal_json["name"]
    for i in range(EXPERIMENT_REPEAT):
        if main(question_path, prompt_path, chal_json):
            success += 1
    
    with open("results.txt", "a+") as f: 
        res = f"Challenge: {chal_name}, Success: {success}/{EXPERIMENT_REPEAT}\n"
        f.write(res)
        print(res)
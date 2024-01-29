import llm_ctf.mixtral_task as mixtral
import sys
import os
import json

def main(question_path, prompt_path, chal_config):

    
    mixtral_task = mixtral.MixtralTask(question_path=question_path, 
                                       task_config=chal_config,
                                       url_path="./keys/mixtral_api.txt")
    mixtral_task.init_task()
    # resp = mixtral_task.task_prompt(prompt=prompt_path, use_file=True)
    print("============================== RESPONSE FROM MODEL ==============================")
    # print(resp)
    # mixtral_task.save_code(resp)
    # mixtral_task.validate_sol(resp)
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <question_path> <prompt_path>")
        sys.exit(1)
        
    question_path = str(sys.argv[1])
    prompt_path = str(sys.argv[2])
    with open(os.path.join(question_path, "challenge.json"), 'r') as f:
        chal_json = json.load(f)
    
    main(question_path, prompt_path, chal_json)
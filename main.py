import llm_ctf.mixtral_task as mixtral

def main():
    
    mixtral_task = mixtral.MixtralTask(question_path="/home/ms12416/projects/LLM_CTF/questions/rev/rebug 1", 
                                       task_name="rebug 1",
                                       url_path="/home/ms12416/projects/LLM_CTF/keys/mixtral_api.txt")
    resp = mixtral_task.task_prompt(prompt="/home/ms12416/projects/LLM_CTF/experiments/prompts_open/rev/rebug1.txt", use_file=True)
    print("============================== RESPONSE FROM MODEL ==============================")
    print(resp)
    mixtral_task.save_code(resp)
    mixtral_task.validate_sol(resp)
    
if __name__ == "__main__":
    main()
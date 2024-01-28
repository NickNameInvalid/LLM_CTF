import llm_ctf.mixtral_task

def main():
    
    mixtral_task = mixtral.MixtralTask(question_path="/Users/sofijajancheska/Documents/GitHub/LLM_CTF/questions/misc/linear_aggressor", 
                                       task_name="linear_aggressor",
                                       url_path="/Users/sofijajancheska/Documents/GitHub/LLM_CTF/keys/mixtral_api.txt")
    resp = mixtral_task.task_prompt(prompt="/Users/sofijajancheska/Documents/GitHub/LLM_CTF/experiments/prompts_open/misc/linear_aggressor.txt", use_file=True)
    print("============================== RESPONSE FROM MODEL ==============================")
    print(resp)
    mixtral_task.save_code(resp)
    mixtral_task.validate_sol(resp)
    
if __name__ == "__main__":
    main()
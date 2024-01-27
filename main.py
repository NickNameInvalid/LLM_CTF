import llm_ctf.mixtral_task as mixtral

def main():
    model = mixtral.mixtral_init(url_path="/home/ms12416/projects/LLM_CTF/keys/mixtral_api.txt")
    resp = mixtral.task_prompt(model, prompt="/home/ms12416/projects/LLM_CTF/experiments/prompts_open/rev/baby's_third.txt", use_file=True)
    mixtral.save_code(resp, save_path="/home/ms12416/projects/LLM_CTF/questions/rev/baby's third")
    print(resp)
    
if __name__ == "__main__":
    main()
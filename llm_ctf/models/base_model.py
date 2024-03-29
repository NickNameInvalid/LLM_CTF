class BaseModel:
    def __init__(self, model_id: str, url_path=None, key_path=None) -> None:
        self.url, self.key = "EMPTY", "EMPTY"
        self.model_id = model_id
        self.client = None
        
        # self.system_prompt = ""
        # self.user_prompts = []
        # self.client_resp = []
        # self.prompt_cache = ""
    
    def generate(self, prompt, use_file=False, temperature=0.8, top_p=0.9):
        raise NotImplementedError
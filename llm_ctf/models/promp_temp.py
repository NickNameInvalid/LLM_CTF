def llama_template(prompts, type) -> str:
    if type == "sys":
        return "<s>[INST] <<SYS>>\n{{ {} }}\n<</SYS>>".format(prompts)
    elif type == "usr":
        return "{{ {} }} [/INST]".format(prompts)
    elif type == "answer":
        return "{{ {} }} </s><s>[INST]".format(prompts)
    else:
        raise ValueError("type must be one of 'sys', 'usr', or 'answer'")
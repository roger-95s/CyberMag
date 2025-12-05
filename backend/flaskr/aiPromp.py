import json
import os


def file_open(datas):
    """
    Open json file function
    """
    content_prompt = [] 
    # Join path components
    prompt_path = os.path.join(
        os.path.dirname(__file__), 
        "../flaskr/cyberattack_analysis_prompt.json",
    )
    # print(f"File path: {prompt_path}")
    # Check if a file exists
    if os.path.exists(prompt_path):
        print(f"{os.path.basename(prompt_path)} exists.")
    else:
        print(f"{os.path.basename(prompt_path)} does not exist.")

    with open(prompt_path, encoding="utf-8") as f:
        prompt_template = json.load(f)
        # print(f"Json info load: {prompt_template}")
        content_prompt =f"{prompt_template['description']}Article:{datas}Instructions:{json.dumps(prompt_template['instructions'], indent=2, ensure_ascii=False)}"
        # print(f"content prompt: {content_prompt}")
    return content_prompt


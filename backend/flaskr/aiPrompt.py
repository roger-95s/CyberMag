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

    with open(prompt_path) as f:
        prompt_template = json.load(f)
        content_prompt = f""" \n
        description: {prompt_template['description']} \n
        Instructions: {prompt_template.get('instructions')} \n 
        article data content: {datas}
        """

        # print(f"content prompt: {type(content_prompt)}: {content_prompt}")
    return content_prompt
    

"""
"site_name": {datas['site_name']}, \n 
        "title": {datas['title']}, \n 
        "url": {datas['site_name']}, \n 
        "content": {datas['content']}, \n   
"""
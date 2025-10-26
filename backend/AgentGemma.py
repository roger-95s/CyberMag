
from ollama import generate
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
        "../backend/cyberattack_analysis_prompt.json",
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
        content_prompt =f"{prompt_template['description']}\n\nArticle:\n{datas}\n\nInstructions:\n{json.dumps(prompt_template['instructions'], indent=2, ensure_ascii=False)}"
    
    return content_prompt


# Function that handle ai work
def gemma_cyber_analyst(prompt, max_chunks=None):
    """
    Generate Cybersecurity analysis from the Gemma3
    :param prompt: Full text prompt to send to the LLM.
    :param max_chunks: Limit the number of streamed chunks.
    :return: Complete response as a string.
    """
    print("==== Generating Analysis ====")
    response_text = ""

    try:
        for i, chunk in enumerate(generate("gemma3", prompt, stream=True)):
            response_text += chunk.get("response", "")
            print(chunk.get("response", ""), end="", flush=True)
            if max_chunks and (i + 1) >= max_chunks:
                break
    except Exception as e:
        print(f"Error generating analysis: {e}")
        return None


# save ai output on data base


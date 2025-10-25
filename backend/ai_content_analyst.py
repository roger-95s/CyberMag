from ollama import generate
from .content import data
import json
import os


print("AI ==================================================!! ")


def file_open():
    """
    Open json file function
    """
    prompt = []

    # Join path components
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        "/home/hackme/portfolio/cybermag/backend/cyberattack_analysis_prompt.json",
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
    prompt = f"{prompt_template['description']}\n\nArticle:\n{data}\n\nInstructions:\n{json.dumps(prompt_template['instructions'], indent=2, ensure_ascii=False)}"

    return prompt


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
            # print(f"Response_text: {response_text}")
            # print()
            # print("AI ==================================================!! ")
            print(chunk.get("response", ""), end="", flush=True)
            # print()
            # print("AI ==================================================!! ")

            if max_chunks and (i + 1) >= max_chunks:
                break

    except Exception as e:
        print(f"Error generating analysis: {e}")
        return None


# save ai output on data base
# def


# Main code
prompt = file_open()
# print(f"Prompt: {prompt}")

# Call file_open fucn
file_open()

# Calling gemma3
gemma_cyber_analyst(prompt=prompt, max_chunks=None)

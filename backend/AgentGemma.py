
from ollama import generate


# Function that handle ai work
def gemma_cyber_analyst(prompt, max_chunks=None):
    """
    Generate Cybersecurity analysis from the Gemma3
    :param prompt: Full text prompt to send to the LLM.
    :param max_chunks: Limit the number of streamed chunks.
    :return: Complete response as a string.
    """
    print("==== Gemma3 Generating Analysis ====")
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

    return response_text


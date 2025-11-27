
from ollama import generate



# Function that handle ai work
def gemma_cyber_analyst(prompt, max_chunks=None):
    
    response_text = ""

    try:
        print()
        print("==== Gemma3 Generating Analysis ====")
        for i, chunk in enumerate(generate("gemma3:1b", prompt, stream=True)):
            response_text += chunk.get("response", "")
            print(chunk.get("response", ""), end="", flush=True)
            if max_chunks and (i + 1) >= max_chunks:
                break
    except Exception as e:
        print(f"Error generating analysis: {e}")
        return None

    return response_text


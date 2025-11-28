from ollama import generate

# Function that handle ai work
def gemma_agent_verifier(prompt, max_chunks=None):
    
    response_text = ""

    try:
        print("==== Gemma Agent Verifier Generating Response ====")
        for i, chunk in enumerate(generate("gemma3:1b", prompt, stream=True)):
            response_text += chunk.get("response", "")
            print(chunk.get("response", ""), end="", flush=True)
            if max_chunks and (i + 1) >= max_chunks:
                break
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

    return response_text

# Call the function to get the response
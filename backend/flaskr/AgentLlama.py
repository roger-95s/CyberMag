from ollama import chat
from .LlmReportsFormat import ReportsFormat


# Function that handle ai work
def llama_cyber_analyst(prompt):

    # report_card = {}
    try:
        print()
        print("==== Llama 3.2 Generating Analysis ====")
        response = chat(
            messages=[
                    {
                        'role': 'user',
                        'content': str(prompt), 
                    }
                    ],
            model='llama3.2:3b',
            format=ReportsFormat.model_json_schema(),
            )
        if response.message.content is None:
            print("Error: Received None content from AI response")
            return None
        report_card = ReportsFormat.model_validate_json(response.message.content)
        # print(report_card)
    except Exception as e:
        print(f"Error generating analysis: {e}")
        return None

    return report_card.__dict__


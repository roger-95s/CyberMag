from ollama import chat
from .modelsbase import ReportsFormat


# Function that handle ai work
def deepseek_cyber_analyst(prompt):

    # report_card = {}
    try:
        print()
        print("==== Deepseek Generating Analysis ====")
        response = chat(
            messages=[
                    {
                        'role': 'user',
                        'content': str(prompt), 
                    }
                    ],
            model='deepseek-r1:1.5b',
            format=ReportsFormat.model_json_schema(),
            )
        report_card = ReportsFormat.model_validate_json(response.message.content)
        print(report_card)
    except Exception as e:
        print(f"Error generating analysis: {e}")
        return None

    return report_card.__dict__


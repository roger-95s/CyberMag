from ollama import chat
from .LlmReportsFormat import ReportsFormat



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
        if response.message.content is None:
            print("Error: Received None content from AI response")
            return None
        report_card = ReportsFormat.model_validate_json(response.message.content).__dict__
        # print(f'type(report_card): {type(report_card)}')
        # print()

    except Exception as e:
        print(f"Error generating analysis: {e}")
        return None

    return report_card
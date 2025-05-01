import os
import json
import requests

def analyze_article(article):
    api_key = os.getenv("OPENROUTER_API_KEY")

    prompt = f"""
    You are a cybersecurity analyst.

    Please analyze the following cybersecurity URL and take the latest article title, and full content.

    URL: {article['url']}

    Provide the following: 
    0. A Full analysis of the content.
    1. A 5-7 sentence summary of what happened, how to be safe, and how to prevent future attacks.
    2. A risk level: Low, Medium, High, or Critical.

    Respond in this format:
    Analysis: ...
    Summary: ...
    Risk Level: ...
    """

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "CyberMag Testing",
            },
            data=json.dumps({
                "model": "nvidia/llama-3.1-nemotron-ultra-253b-v1:free",
                "messages": [
                    {"role": "system", "content": "You are an expert cybersecurity analyst."},
                    {"role": "user", "content": prompt}
                ]
            })
        )

        json_data = response.json()

        if "choices" not in json_data:
            print("❌ LLM response error:", json_data)
            return {
                "url": article["url"],
                "title": article.get("title", "Unknown"),
                "analysis": "Unknown analysis",
                "summary": "LLM error occurred",
                "risk_level": "Unknown"
            }

        reply = json_data["choices"][0]["message"]["content"]

        analysis = "Not available"
        summary = "Not available"
        risk_level = "Unknown"

        for line in reply.splitlines():
            lower_line = line.lower()
            if lower_line.startswith("analysis:"):
                analysis = line.split(":", 1)[-1].strip()
            elif lower_line.startswith("summary:"):
                summary = line.split(":", 1)[-1].strip()
            elif lower_line.startswith("risk level:"):
                risk_level = line.split(":", 1)[-1].strip()

        return {
            "url": article["url"],
            "title": article.get("title", "Unknown"),
            "analysis": analysis,
            "summary": summary,
            "risk_level": risk_level
        }

    except Exception as e:
        print(f"❌ Error during LLM request: {e}")
        import traceback
        traceback.print_exc()
        return {
            "url": article["url"],
            "title": article.get("title", "Unknown"),
            "analysis": "Error implementing LLM analysis",
            "summary": "Error unable to generate summary.",
            "risk_level": "Unknown"
        }

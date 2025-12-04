from ollama import generate
import json
from .models import Cybersecurity_Reports, db


def clean_ai_output(text: str) -> str:
    text = text.strip()

    # Remove markdown JSON fences
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    # If the model adds commentary before JSON, extract JSON:
    first_brace = text.find("{")
    last_brace = text.rfind("}")

    if first_brace != -1 and last_brace != -1:
        return text[first_brace:last_brace+1]

    return text  # fallback


def gemma_agent_verifier(prompt, max_chunks=None):
    import json
    response_text = ""

    print("==== Gemma Agent Verifier Generating Response ====")
    for i, chunk in enumerate(generate("gemma3:1b", prompt, stream=True)):
     
        response_text += chunk.get("response", "")
        # print(chunk.get("response", ""), end="", flush=True)
    
        if max_chunks and (i + 1) >= max_chunks:
            break

    # Strip markdown, logs, and non-JSON parts
    cleaned = clean_ai_output(response_text)
    reports(meta_data=cleaned)
    try:
        parsed_json = json.loads(cleaned)
        print(f"parsed_json: {parsed_json}")
        

        return parsed_json

    except Exception as e:
        print("\n❌ JSON Parse Error in Verifier:", e)
        return None


# Save function 
def reports(meta_data):

    if not meta_data:
        print("❌ No metadata received")
        return None

    # Extract required fields
    url = meta_data.get("sections", {}).get("article_metadata", {}).get("article_url")
    title = meta_data.get("sections", {}).get("article_metadata", {}).get("title")
    name = meta_data.get("sections", {}).get("article_metadata", {}).get("source")
    summary = meta_data.get("sections", {}).get("executive_summary")
    ai_name = meta_data.get("sections", {}).get("ai_agent_name", "Gemma Agent Verifier")

    if not url:
        print("❌ Cannot save report — missing URL")
        return None

    # Check for duplicates
    existing = Cybersecurity_Reports.query.filter_by(url=url).first()
    if existing:
        print(f"⚠️ Duplicate skipped: {url}")
        return existing

    try:
        new_report = Cybersecurity_Reports(
            agent_name = ai_name,
            url = url,
            site_name = name,
            title = title,
            publication_date = None,  # Optional unless AI provides it
            article_type = meta_data["sections"]["article_metadata"].get("article_type"),
            risk_level = meta_data["sections"]["article_metadata"].get("risk_level"),
            summary = summary,
            analysis_payload = meta_data,  # Save full JSON
        )

        db.session.add(new_report)
        db.session.commit()

        print(f"✅ Saved Report: {title}")

        return new_report

    except Exception as e:
        db.session.rollback()
        print(f"❌ Database Commit Error: {e}")
        return None



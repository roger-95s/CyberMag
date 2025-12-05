from .models import Cybersecurity_Reports, db
import json
import re


def extract_clean_json(text):

    if not isinstance(text, str):
        print("❌ LLM output is not a string")
        return None

    # Remove backticks if the model still added them
    cleaned = text.replace("```json", "").replace("```", "").strip()

    # Find and extract first JSON object
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        print("❌ Could not locate JSON object in LLM output.")
        print("Raw output was:\n", text[:500])
        return None

    json_text = match.group(0)

    try:
        return json.loads(json_text)
    except Exception as e:
        print("❌ JSON decoding error:", e)
        print("JSON text:\n", json_text)
        return None

    
def ai_responses_save(meta_data):
    if not meta_data:
        print("❌ No meta_data received.")
        return None

    # Extract using your REAL JSON structure
    site_name = meta_data.get("site_name")
    title = meta_data.get("title")
    publication_date = meta_data.get("publication_date", None)
    article_type = meta_data.get("article_type")
    risk_level = meta_data.get("risk_level")
    summary = meta_data.get("summary")
    url = meta_data.get("url")

    analysis_payload = meta_data.get("sections")
    print("EXTRACTED FIELDS:", site_name, title, publication_date, risk_level, url)

    # Validate required fields BEFORE saving
    required_fields = [site_name, title, publication_date, risk_level, url]
    if any(field in (None, "") for field in required_fields):
        print("❌ Missing required fields:", required_fields)
        return None

    # Check duplicates
    existing = Cybersecurity_Reports.query.filter_by(url=url).first()
    if existing:
        print(f"⚠️ Duplicate skipped: {url}")
        return existing

    # Save report
    report = Cybersecurity_Reports(
        agent_name=None,  # or fill later
        site_name=site_name,
        title=title,
        publication_date=publication_date,
        article_type=article_type,
        risk_level=risk_level,
        summary=summary,
        url=url,
        analysis_payload=analysis_payload
    )

    db.session.add(report)
    db.session.commit()

    print(f"✅ Saved report for URL: {url}")
    return report
from .models import Cybersecurity_Reports, db
from datetime import datetime, timezone
import json

def cybersecurity_reports_save_tool(report_data: dict):
    """
    Save normalized report data to the database.
    
    Args:
        report_data: Normalized report dictionary
        
    Raises:
        ValueError: If required fields are missing
    """
    REQUIRED_FIELDS = ["agent_name", "site_name", "url", "title"]
    
    # Check for missing or empty required fields
    missing = [f for f in REQUIRED_FIELDS if not report_data.get(f)]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
    
    # Convert analysis_payload to JSON string if it's a dict
    analysis_payload = report_data.get("analysis_payload")
    if isinstance(analysis_payload, dict):
        analysis_payload = json.dumps(analysis_payload)
    elif analysis_payload is None:
        analysis_payload = json.dumps({})
    
    # Convert main_summary to string if it's a list
    summary = report_data.get("summary")
    if isinstance(summary, list):
        summary = "\n".join(str(item) for item in summary if item)
    elif summary is None:
        summary = ""
    
    new_report = Cybersecurity_Reports(
        agent_name=report_data["agent_name"],
        url=report_data["url"],
        site_name=report_data["site_name"],
        title=report_data["title"],
        publication_date=report_data.get("publication_date") or None,
        article_type=report_data.get("article_type") or None,
        risk_level=report_data.get("risk_level") or "unknown",
        summary=summary,
        analysis_payload=analysis_payload,
        created_at=datetime.now(timezone.utc)  # Set UTC timestamp
    )
    
    db.session.add(new_report)
    db.session.commit()
    
    return new_report
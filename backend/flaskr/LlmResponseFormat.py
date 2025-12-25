from .Cybersecurity_Reports_save_tool import cybersecurity_reports_save_tool


def func_handle_llm_caller_return(response_data: dict):
    """
    Process and save responses from multiple agents.
    
    Args:
        response_data: Dictionary mapping agent names to their responses
        
    Returns:
        List of normalized reports that were saved
    """
    saved_reports = []
    
    # Loop through each agent's response
    for agent_name, agent_data in response_data.items():
        # Skip if agent_data is None or empty
        if not agent_data:
            print(f"Warning: No data received from {agent_name}, skipping...")
            continue
        
        # Skip if agent_data is not a dictionary
        if not isinstance(agent_data, dict):
            print(f"Warning: Invalid data type from {agent_name}: {type(agent_data)}, skipping...")
            continue
        
        try:
            # Normalize the report with correct parameters
            normalized = normalize_report(
                agent_name=agent_name,    # Pass the KEY (e.g., "Agentgemma")
                raw=agent_data            # Pass the VALUE (the response dict)
            )
            
            # Save to database
            cybersecurity_reports_save_tool(normalized)
            saved_reports.append(normalized)
            print(f"Successfully saved report for {agent_name}")
            
        except ValueError as ve:
            print(f"Validation error for {agent_name}: {ve}")
            continue
        except Exception as e:
            print(f"Error processing report for {agent_name}: {e}")
            continue
    
    return saved_reports


def normalize_report(agent_name: str, raw: dict):
    """
    Normalize agent response data into a standard format.
    
    Args:
        agent_name: Name of the agent (e.g., "Agentgemma")
        raw: Raw response dictionary from the agent
        
    Returns:
        Normalized report dictionary
    """
    if not raw:
        raw = {}
    
    return {
        "agent_name": agent_name,
        "site_name": raw.get("site_name", ""),
        "url": raw.get("url", ""),
        "title": raw.get("title", ""),
        "publication_date": raw.get("publication_date", ""),
        "article_type": raw.get("article_type", ""),
        "risk_level": raw.get("risk_level", "unknown"),
        "main_summary": (
            raw.get("main_summary")
            or raw.get("executive_summary")
            or ""
        ),
        "analysis_payload": raw.get("sections") or raw.get("analysis_payload") or {},
    }



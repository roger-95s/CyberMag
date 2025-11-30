from ollama import generate
from .models import cybersecurity_reports, db



# Function that handle ai work
def gemma_agent_verifier(prompt, max_chunks=None):
    
    response_text = ""

    try:
        print("==== Gemma Agent Verifier Generating Response ====")
        for i, chunk in enumerate(generate("gemma3:1b", prompt, stream=True)):
            response_text += chunk.get("response", "")
            print(chunk.get("response", ""), end="", flush=True)
            
            #  target data structure
            data = response_text.get("sections", {})
            meta = response_text.get("article_metadata", {})  

            # Check for duplications 
            try:
                exits = cybersecurity_reports.query.filter_by(id=id).first()

                if not exit:
                    new_report = cybersecurity_reports( 
                    # Map the metadata fields
                    # ReportCard Column fields
                    agent = data.get("ai_agent_name", "UNKNOWN"),
                    url = meta.get("article_url", "UNKNOWN_URL"),
                    site_name = meta.get("source", "UNKNOWN"),  
                    title = meta.get("title", "UNKNOWN"),
                    risk_level = meta.get("risk_level", "UNKNOWN"),  
                    publication_date = data.get("publication_date", None),
                    summary = data.get("executive_summary", "UNKNOWN"),

                    # Full analysis payload as JSONB
                    analysis_payload = data 
                    )
                    
                    # save response 
                    db.session.add(new_report)

                else:
                    # Optional: Print skipped duplicates
                    pass

            except Exception as e:
                print(f"⚠️ Error preparing article {e}") 


            try:
            # 4. Commit all new articles at once (Bulk commit)
                db.session.commit()
                print(f" Success!! ")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Database Commit Error: {e}")
            if max_chunks and (i + 1) >= max_chunks:
                break
        
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

    return response_text


   
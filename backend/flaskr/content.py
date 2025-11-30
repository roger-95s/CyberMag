"""
content fetch articles' content from sites and save them to the database.
This script uses BeautifulSoup to parse HTML and extract articles' content.
It iterates over a predefined list of sites, fetches the HTML content,
extracts the required data, and saves it to the database.
"""
import traceback
from . import create_app
from .scraper import get_response
from bs4 import BeautifulSoup, Tag
# import WebsiteFetch 
from .models import WebsiteFetch
from .tag_guide import list_of_sites
# import aiPromp, AgentLlama, AgentGemma, AgentDeepseek
from .aiPromp import file_open 
from .AgentLlama import llama_cyber_analyst
from .AgentGemma import gemma_cyber_analyst
from .AgentDeepseek import deepseek_cyber_analyst
from .AgentGemmaVerifyier import gemma_agent_verifier


# set a limit of site for request 
LIMIT = 1

# fetch for articles content_selector tags
def fetch_content_data(soup_obj: BeautifulSoup, selector_map: dict, limit: int) -> dict:
    """fetch articles' content using the provided selectors"""
    try:
        # print(f"🔍 Selector map structure: {selector_map}")
        # check if content_selector exists
        if "content_selector" not in selector_map:
            print("❌ 'content_selector' key not found in selector_map")
            return {"content": []}

        # Extract selector components safely
        content_tag = selector_map["content_selector"]["tag"]
        content_ancestor_tag = selector_map["content_selector"]["ancestor_tag"]
        content_class = selector_map["content_selector"]["ancestor_class"]
        ancestor_containers = soup_obj.find_all(
            content_ancestor_tag, class_=content_class, limit=limit
        )

        # print(
        #     f"Found {len(ancestor_containers)} ancestor containers with class '{content_class}'"
        # )

        content_items = []

        for container in ancestor_containers:
            if isinstance(container, Tag):
                items = container.find_all(content_tag)
                content_items.extend(items)
            # print(f"📦{container}")

        # print(
        #     f"Found {len(content_items)} {content_tag} tags within ancestor containers"
        # )

        contents = []
        for content in content_items:
            text = content.get_text(strip=True)
            # print(
            #     f"Content text: {text[:100]}..."
            #     if len(text) > 100
            #     else f"Content text: {text}"
            # )
            if text:
                contents.append(text)
        if not contents:
            return {"content": []}

        return {"content": contents}

    except ImportError as e:
        print(f"❌ Error during fetching article content: {e}")
        traceback.print_exc()
        return {"content": []}


# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    # 1. Initialize the App
    app = create_app()

    # 2. Create the Context (The "Bridge" to the DB)
    with app.app_context():
        print("🚀 Starting Content Fetcher...")

        # --- A. Database Fetch ---
        # Fetch all articles that we saved in the previous step
        # Ideally, you might want to filter for articles that haven't been analyzed yet
        db_articles = WebsiteFetch.query.all()
        
        print(f"\n🔍 Fetched {len(db_articles)} articles from the database for processing.")

        # Build a quick lookup dictionary from list_of_sites
        site_lookup = {site["name"]: site for site in list_of_sites}

        # Define limit for testing (Process specific slice, e.g., 2nd item only)
        # Change to db_articles[:] to process all
        batch_to_process = db_articles[1:2] 

        # --- B. Main Loop ---
        for i, row in enumerate(batch_to_process, start=1):
            
            # FIX: Access attributes via dot notation, NOT .get()
            name = row.site_name
            title = row.title
            url = row.url

            # Debugging and visual structure
            print(f"\n{'=' * 50}")
            print(f"⭐ Site name: {name}")
            print(f"📄 Processing article {i}/{len(batch_to_process)}")
            print(f"🔗 URL: {url}")

            # --- C. Selector Lookup ---
            site_config = site_lookup.get(name)
            if not site_config:
                print(f"❌ No configuration found for site '{name}' in tag_guide.")
                continue
            
            selectors = site_config.get("selectors", {})
            if not selectors:
                print(f"❌ No selectors defined for '{name}'")
                continue

            # --- D. Fetch HTML (Soup) ---
            soup = get_response(url.strip())
            if not soup:
                print(f"❌ Could not get HTML soup for {url}")
                continue
            
            print(f"✅ HTML fetched successfully.")

            # --- E. Extract Content ---
            # assuming fetch_content_data is defined elsewhere
            content_data = fetch_content_data(soup, selector_map=selectors, limit=10)
            
            if not content_data:
                print("❌ No content extracted from HTML.")
                continue

            print(f"✅ Content extraction successful.")

            # --- F. Prepare for AI Agent ---
            try:
                # Structure the data cleanly for the AI prompt function
                # We combine the DB data with the Scraped data
                combined_data = {
                    "site_name": name,
                    "title": title,
                    "scraped_content": content_data
                }

                # Generate the Prompt
                # assuming file_open() formats the prompt string
                agent_prompt = file_open(datas=combined_data) 

                if agent_prompt:
                    print("\n🤖 ==== AI Tool Execution Started ====")
                    print()
                    try: 
                        # Preferred model calls
                        response = {
                            "llama_response": llama_cyber_analyst(prompt=agent_prompt), 
                            "deepseek_response": deepseek_cyber_analyst(prompt=agent_prompt), 
                            "gemma_response": gemma_cyber_analyst(prompt=agent_prompt),
                        }
                        # print(f" Response_text: {response_text}")
                        if response is None:
                            print("❌ No responses from agents to verify.")
                            break 
                        gemma_agent_verifier(prompt=f"""
                            You are an expert AI Verification Engine. Your goal is to validate the outputs of three distinct AI agents (Llama, DeepSeek, Gemma) to ensure completeness and semantic consistency.

                            **INPUT DATA:**
                            Original Context: {combined_data}
                            Agent Responses: {response}

                            **TASK:**
                            1. **Completeness Check:** Verify that 'llama_response', 'deepseek_response', and 'gemma_response' are all present and not null/empty.
                            2. **Consistency Check:** Compare the content of the three responses. They do not need to be identical word-for-word, but they must agree on the core facts and conclusion based on the input data.

                            **OUTPUT FORMAT:**
                            You must respond with a SINGLE valid JSON object. Do not include markdown formatting or explanations outside the JSON.

                            **Logic:**
                            - IF any agent failed to respond OR the responses contradict each other:
                            
                                "status": "failure",
                                "reason": "Missing response OR Inconsistent conclusions",
                                "details": 
                                    "analysis": "Briefly explain the discrepancy or missing data here."
                                
                            

                            - IF all agents responded AND agreed:
                            
                                "status": "success",
                                "next_step": 
                                    "agent_prompt": "{agent_prompt}",
                                    "article_url": "{url}"
                                
                        
                            Please provide your analysis now.
                        """ )

                        # Print mock result for demonstration purposes 
                        # print("... (AI Model would run here) ...")
                        # print("✅ AI Analysis Complete (Mocked)")
                        
                    except Exception as e:
                        print(f"❌ Error during AI tool execution: {e}")
                else:
                    print("❌ Generated prompt was empty.")

            except Exception as e:
                print(f"❌ Error preparing data for AI: {e}")
                traceback.print_exc()

        print("\n🏁 Content Fetcher & Analysis Job Finished.")


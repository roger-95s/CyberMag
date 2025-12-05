import os
import traceback
from .aiPromp import file_open
from .AIResponsesSave import ai_responses_save, extract_clean_json
from .AgentGemma import gemma_cyber_analyst
from .AgentLlama import llama_cyber_analyst
from .AgentDeepseek import deepseek_cyber_analyst
from .scraper import get_response, fetch_data, save_articles_to_db
from .content import fetch_content_data
from .tag_guide import list_of_sites
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from .models import db, WebsiteFetch, Cybersecurity_Reports

def create_app(test_config=None):
    # create and configure the app 
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        # Flask-SQLAlchemy needs this URI to connect to the database
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'cybermag.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=True
    )

    if test_config:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # --- INITIALIZE EXTENSIONS ---
    db.init_app(app)
    migrate = Migrate(app, db)
    # -----------------------------


    # --- SIMPLE ROUTE FOR TESTING ---
    @app.route('/db')
    def hello():
        reports = Cybersecurity_Reports().query.all()

        meta_data = [a.to_dict() for a in reports]
        return jsonify({"success": True, "article": meta_data})


    # Helper function (Updated to use ORM)
    def get_paginated_articles(page: int, limit: int):
        # Use SQLAlchemy query
        pagination = WebsiteFetch.query.paginate(page=page, per_page=limit, error_out=False)
        
        # Convert objects to dicts using the helper we made in models.py
        articles_data = [item.to_dict() for item in pagination.items]
        return articles_data, pagination.pages


    # --- API ROUTES --- Site Home Page 
    @app.route("/api/home", methods=["POST", "GET"])
    def home():
        welcome_message = "👨‍💻⚒️ Welcome to CyberMag!"
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 9))

        try:
            paginated_articles, total_pages = get_paginated_articles(page, limit)
            
            if paginated_articles:
                welcome_message += f" Latest {len(paginated_articles)} Articles."
            else:
                welcome_message += " No articles found."

            return jsonify({
                "success": True,
                "message": welcome_message,
                "total_pages": total_pages,
                "current_page": page,
                "articles": paginated_articles
            }), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500


    # --- API ROUTES --- Site Posts Page 
    @app.route("/api/posts", methods=["GET"])
    def reports_card():
        try:
            # Fetch all records via ORM
            articles = WebsiteFetch.query.all()
            articles_data = [a.to_dict() for a in articles]
            
            return jsonify({
                "success": True, 
                "articles_data": articles_data
            }), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500


    # --- API ROUTES --- Single Post Page
    @app.route("/api/post/<int:post_id>", methods=["GET"])
    def get_single_report(post_id):
        try:
            articles = WebsiteFetch.query.all()
            article = next((a for a in articles if a.id == post_id), None)
            if article:
                return jsonify({"success": True, "article": article.to_dict()}), 200
            # Return 404 if article not found
            return jsonify({"success": False, "error": "Article not found"}), 404
        except ImportError as e:
            articles = None
            # Handle ImportError if models.py is not found or has issues
            print(f"❌ Error fetching report: {e}")
            return jsonify({"success": False, "error": str(e)}), 500
    

    # --- Calling content.py ---
    @app.route("/api/scraper", methods=["GET"])
    def backend_scraper_caller():
        LIMIT = 15  # set a limit of site for request
        for site in list_of_sites:
            site_name = site.get("name", "Unknown")
            url = site.get("url")
            selectors = site.get("selectors")
            if url and selectors:
                soup = get_response(url)
                if soup:
                    data = fetch_data(soup, selectors, limit=LIMIT)
                    if data.get("title"):
                        save_articles_to_db(data, name=site_name)
                    else:
                        print(f"❌ No data found for {site_name}")
            else:
                print(f"⚠️ Skipping {site_name} — missing URL or selectors.")

        result = data
        print(f"🏁 Scraper finished. {result}")

        return result

    # --- Calling content.py ---
    @app.route("/api/scraper_content", methods=["GET"])
    def backend_content_caller():
        LIMIT = 1 # set a limit of site for request 

        # Query all website_fetch name, url and title 
        db_articles = WebsiteFetch.query.all()
        
        if not db_articles:
            print("No areticle found in the db query")     
        # Print db_articles len 
        print(f"\n Fetched {len(db_articles)} articles from the database for processing.")

        # Build a quick lookup dictionary from list_of_sites
        site_lookup = {site["name"]: site for site in list_of_sites}

        # Define limit for testing (Process specific slice, e.g., 2nd item only)
        # Change to db_articles[:] to process all
        batch_to_process = db_articles[0:1]

        # --- Main Loop ---
        for i, row in enumerate(batch_to_process, start=1):
            
            # Access attributes and assign site_name, title, and url  
            name = row.site_name
            title = row.title
            url = row.url

            # Debugging and visual structure
            print(f"\n{'=' * 50}")
            print(f"⭐ Site name: {name}")
            print(f"📄 Processing article {i}/{len(batch_to_process)}")
            print(f"Titles: {title}")
            print(f"🔗 URL: {url}")

            # --- Selector Lookup ---
            site_config = site_lookup.get(name)
            if not site_config:
                print(f"❌ No configuration found for site '{name}' in tag_guide.")
                continue
            
            selectors = site_config.get("selectors", {})
            if not selectors:
                print(f"❌ No selectors defined for '{name}'")
                continue

            # --- Fetch HTML (Soup) ---
            soup = get_response(url.strip())
            if not soup:
                print(f"❌ Could not get HTML soup for {url}")
                continue
            
            print(f"✅ HTML fetched successfully.")

            # --- Extract Content ---
            # assuming fetch_content_data is defined elsewhere
            content_data = fetch_content_data(soup, selector_map=selectors, limit=LIMIT)
            
            if not content_data:
                print("❌ No content extracted from HTML.")
                continue

            print(f"✅ Content extraction successful.")

            # --- Prepare for AI Agent ---
            try:
                # Structure the data cleanly for the AI prompt function
                # We combine the DB data with the Scraped data
                combined_data = {
                    "site_name": name,
                    "title": title,
                    "url": url,
                    "scraped_content": content_data,
                }
            except Exception as e:
                print(f"❌ Error preparing data for AI: {e}")
                traceback.print_exc()
            # Assign combined_data to file_open and store it into prompt_result 
            prompt_result = file_open(datas=combined_data)
        
        return prompt_result
    
    
    # --- Calling content.py ---
    @app.route("/api/llm_response", methods=["GET"])
    def llm_caller():
        PROMPT = PROMPT = f"""
                            You are a cybersecurity analysis engine.
                            
                            Your ONLY output must be a valid JSON object.
                            Do NOT include:
                            - markdown code fences (```json)
                            - explanations
                            - text before or after the JSON
                            - comments
                            - reasoning
                            
                            Your response MUST be ONLY a JSON object matching EXACTLY this structure:
                            
                            {{
                              "site_name": "",
                              "title": "",
                              "publication_date": "",
                              "article_type": "",
                              "risk_level": "",
                              "summary": "",
                              "url": "",
                              "analysis": {{}}
                            }}
                            
                            Fill in all fields.
                            Use empty strings "" ONLY if you absolutely cannot determine a field.
                            Make sure the JSON is valid and properly formatted.
                            
                            Now analyze the following article and produce the JSON:
                            {backend_content_caller()}
                            """
 
        try:
            # call deepseek
            # deepseek_response = deepseek_cyber_analyst(prompt=PROMPT)
            
            # call llama
            llama_response = llama_cyber_analyst(prompt=PROMPT)
            
            # call gemma
            # gemma_response = gemma_cyber_analyst(prompt=PROMPT)
            parsed = extract_clean_json(llama_response)
            print(parsed)

            if not parsed:
                return jsonify({"error": "LLM did not return valid JSON"}), 400

            ai_responses_save(parsed)

            # Call gemmaVerifyier
            return jsonify({
                "success": True, 
                # "deepseek_response": str(deepseek_response),
                "llama_response": llama_response,
                # "gemma_response": str(gemma_response),
                }), 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
        
    
    return app
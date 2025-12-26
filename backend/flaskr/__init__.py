import os
import traceback
from .aiPrompt import file_open
# from .AIResponsesSave import ai_responses_save, extract_clean_json
from .AgentGemma import gemma_cyber_analyst
from .AgentLlama import llama_cyber_analyst
from .AgentDeepseek import deepseek_cyber_analyst
from .LlmResponseFormat import func_handle_llm_caller_return, normalize_report
from .scraper import get_response, fetch_data, save_articles_to_db
from .content import fetch_content_data
from .tag_guide import list_of_sites
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from .models import db, WebsiteFetch, Cybersecurity_Reports 
from .ContentUpdate import site_separated_by_name, tags_selectors


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

    # --- TESTING AREA ---
    @app.route('/db')
    def hello():
        reports = Cybersecurity_Reports().query.all()

        meta_data = [a.to_dict() for a in reports]
        return jsonify({"success": True, "article": meta_data})

    @app.route("/api/test_query_by_limit_of_3", methods=["GET"])
    def return_article_limte_of_three():
        # assign function return to result 
        result = site_separated_by_name()

        # return result data
        return result
        
    
    # Helper function (Updated to use ORM)
    # --- API ROUTES --- Site Pagination function
    def get_paginated_articles(page: int, limit: int):
        # Use SQLAlchemy query
        pagination = Cybersecurity_Reports.query.paginate(page=page, per_page=limit, error_out=False)
        # Test and change how to query the report_card 
        # pagination = reports_card.query.paginate(page=page, per_page=limit, error_out=False)
        
        # Convert objects to dicts using the helper we made in models.py
        articles_data = [item.to_dict() for item in pagination.items]
        return articles_data, pagination.pages


    # --- API ROUTES --- Site Home Page 
    @app.route("/api/home", methods=["POST", "GET"])
    def home():
        welcome_message = "👨‍💻⚒️ Welcome to CyberMag!"
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 20))

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
            articles = Cybersecurity_Reports.query.all()
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
            articles = Cybersecurity_Reports.query.all()
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
    def content_caller():   
        LIMIT=3

        content_data_list = []
        articles = site_separated_by_name()

        for data in articles:
            site_name = data.get('site_name')
            title = data.get('title')
            url = data.get('url')

            soup = get_response(url.strip())
            if soup is None:  # ← handle None soup
                print(f"⚠️ Skipping {url}: failed to fetch content")
                continue
            # print(soup)

            # --- Selector Lookup ---
            TheHackerNews = tags_selectors()
            # print(TheHackerNews)
            # print(selectors)
            # get selectors form the hacker news
            selectors = TheHackerNews.get("selectors", {})

            content_data = {
                "content": fetch_content_data(soup, selector_map=selectors, limit=LIMIT).get('content'),
                'site_name': site_name,
                'title':title,
                'url': url,
            }
            content_data_list.append(content_data)
            # print()
            # print(content_data)

        return content_data_list
    

    # --- Prepare for AI Agent ---
    # PROMPT = file_open(datas=combined_data)
    @app.route('/api/prompts_creater')
    def prompts_creater():
        PROMPT_LISTS = []

        # Store the fetched article metadata 
        aritcle_data = content_caller()

        for data in aritcle_data:
            PROMPT_LISTS.append(file_open(datas=data)) 

        return PROMPT_LISTS
    

    # @app.route("/api/llm_response", methods=["GET"])
    # def function_caller_tester():

    #     llm_response = dict(llm = llm_caller())

    #     print(f'llm_response Type: {type(llm_response)}')

        
    #     return {
    #         "status": True,
    #         "saved_agents": llm_response
    #     }, 200


    # --- Calling content.py ---
    @app.route("/api/llm_response", methods=["GET"])
    def llm_caller():
        PROMPT = prompts_creater()
        # print(f"{type(PROMPT)} : {PROMPT[:]}")
        try:
            # call deepseek
            deepseek_response = deepseek_cyber_analyst(prompt=PROMPT[0])
            # # debug reponses form
            print() 
            # print(f"deepseek_response and type: {type(deepseek_response)}: {deepseek_response}")

            # call gemma
            gemma_response = gemma_cyber_analyst(prompt=PROMPT[1])
            # # debug reponses form 
            print()
            # print(f"gemma_response and type: {type(gemma_response)}: {gemma_response}")

            # call llama
            llama_response = llama_cyber_analyst(prompt=PROMPT[2])
            # debug reponses form 
            print()
            # print(f"llama_response and type: {type(llama_response)}: {llama_response}")
            

            all_agents_response = {
                "Agentgemma" : gemma_response,
                "Agentdeepseek" : deepseek_response,
                "Agentllama" : llama_response,
                
            }

            print()
            print(f"{type(all_agents_response)}, {all_agents_response}")

            func_handle_llm_caller_return(response_data=all_agents_response)
            
            return {
                "success": True,
                "responses": all_agents_response,
                }, 200
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
  

    # # --- Calling content.py ---
    # @app.route("/api/scraper_content", methods=["GET"])
    # def backend_content_caller():
    #     LIMIT = 2 # set a limit of site for request 

    #     # Query all website_fetch name, url and title 
    #     db_articles = site_separated_by_name()
    #     # print(f'db_articles: {db_articles}')
        
    #     if not db_articles:
    #         print("❌ Article was not found")     
    #     # Print db_articles len 
        # print(f"\n Fetched {len(db_articles)} articles from the database for processing.")

        # # --- Main Loop ---
        # for i, row in enumerate(db_articles, start=0):
            
        # Access attributes and assign site_name, title, and url  
        # name = site_name
        # title = title
        # url = row.url
        # # Debugging and visual structure
        # print(f"\n{'=' * 50}")
        # print(f"⭐ Site name: {name}")
        # print(f"📄 Processing article {i}/{len(db_articles)}")
        # print(f"Titles: {title}")
        # print(f"🔗 URL: {url}")
        # print(f'📦 Batch_to_process: {batch_to_process}')

        # --- Selector Lookup ---
        # Build a quick lookup dictionary from list_of_sites
        # site_lookup = {site["name"]: site for site in list_of_sites}
        # site_config = site_lookup.get(name)
        # if not site_config:
        #     print(f"❌ No configuration found for site '{name}' in tag_guide.")
        #     continue
        
        # selectors = site_config.get("selectors", {})
        # if not selectors:
        #     print(f"❌ No selectors defined for '{name}'")
        #     continue
        # # --- Fetch HTML (Soup) ---
        # soup = get_response(url.strip())
        # if not soup:
        #     print(f"❌ Could not get HTML soup for {url}")
        #     break
        # # --- Extract Content ---
        # # assuming fetch_content_data is defined elsewhere
        # content_data = fetch_content_data(soup, selector_map=selectors, limit=LIMIT)
        # if not content_data:
        #     print("❌ No content extracted from HTML.")
        #     break
        # print(f"✅ HTML fetched successfully.") 
        # # print(f"✅ Content extraction {content_data}")

        # # --- Prepare for AI Agent ---
        # try:
        #     # Structure the data cleanly for the AI prompt function
        #     # We combine the DB data with the Scraped data
        #     combined_data = {
        #         "site_name": name,
        #         "title": title,
        #         "url": url,
        #         "scraped_content": content_data.get('content'), # find a way to pass content from it source so no extra key is created
        #     }
        #     # Debug
        #     # print()
        #     print(f"Combined_data: {combined_data}")
        #     # AI prompt 
        #     PROMPT = file_open(datas=combined_data)
        #     # Assign combined_data to file_open and store it into prompt_result 
        #     # Debug prompt_result
        #     # print()
        #     # print (f'prompt_result: {prompt_result}')
        #     return {
        #         "combined_data": combined_data,
        #         "success": True,
        #     }, 200
        
        # except Exception as e:
        #     print(f"❌ Error preparing data for AI: {e}")
        #     traceback.print_exc()
        #     return jsonify({"success": False, "error": str(e)}), 500
        
        
    return app
import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from .models import db, WebsiteFetch 

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
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

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
        limit = int(request.args.get("limit", 10))

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
        


    return app
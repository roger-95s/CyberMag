"""Module providing a flaks class and json function python version."""

from .models import get_all_site
from flask import Flask, jsonify, request
from flask_cors import CORS
from .pagination import get_paginated_articles


# Create Flask app
app = Flask(__name__)
CORS(app)


# Route the home page
@app.route("/api/home", methods=["POST", "GET"])
def home() -> tuple:
    """Home route returning a welcome message and 9 articles."""
    # Build a welcome message displaying the app name
    welcome_message = (
        "👨‍💻⚒️ Welcome to CyberMag! "
        "This is an app for managing cybersecurity reports. "
        "Use the /post endpoint or click on a report to see more."
    )
    # Try to display the first 9 articles in the welcome message
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    try:
        # Get paginated articles using helper
        paginated_articles, total_pages = get_paginated_articles(page, limit)

        if not paginated_articles:
            welcome_message += "No article found."
        else:
            welcome_message += f"Latest {len(paginated_articles)} Articles of Cyber Attacks:"

        articles_data = []
        for article in paginated_articles:
            try:
                title = article.get("title", "").lower()
                if "ai" in title:
                    icon = "ai"
                elif "ransomware" in title:
                    icon = "ransomware"
                elif "network" in title:
                    icon = "network"
                elif "threat" in title:
                    icon = "threats"
                elif "global" in title:
                    icon = "globe"
                else:
                    icon = "unknown"

                articles_item = {
                    "analysis": article.get("analysis", "No Analysis"),
                    "summary": article.get("summary", "No Summary"),
                    "risk_level": article.get("risk_level", "Unknown"),
                    "title": article.get("title", "No Title"),
                    "url": article.get("url", "No Urls"),
                    "site_name": article.get("site_name", "No Site Name"),
                    "icon": icon,
                    "id": article.get("id"),
                }
                articles_data.append(articles_item)
            except (KeyError, TypeError) as e:
                print(f"❌ Error processing article: {e}")
                continue

        # Return the welcome message as a JSON response with 200 status code
        return (
            jsonify(
                {
                    "success": True,
                    "message": welcome_message,
                    "articles_data": articles_data,
                    "total_pages": total_pages,
                    "current_page": page,
                }
            ),
            200,
        )
    except ImportError as e:
        # Handle any exception that might occur when fetching analysis
        error_message = welcome_message + f" ❌ Error: {e}"
        print(f"❌ Error fetching analysis: {e}")
        return (
            jsonify({"success": False, "error": error_message}),
            500,
        )


# Route to get all reports
@app.route("/api/post", methods=["GET"])
def post_reports():
    """Function post_reports return True if successful,
    len(articles) and articles, and A list of articles."""
    # try to get all reports from the database
    try:
        articles = get_all_site()
        return (
            jsonify({"success": True, "count": len(articles), "articles": articles}),
            200,
        )
    # Handle ImportError if models.py is not found or has issues
    except ImportError as e:
        return ({"success": False, "error": str(e), "articles": []}), 500


# Uncomment the following lines if you want to add a route to save reports"
# Optional: Add a route to get a single report by ID
@app.route("/api/post/<int:post_id>", methods=["GET"])
def get_single_report(post_id):
    try:
        articles = get_all_site()
        article = next((a for a in articles if a["id"] == post_id), None)
        if article:
            return jsonify({"success": True, "article": article})
        # Return 404 if article not found
        return jsonify({"success": False, "error": "Article not found"}), 404
    except ImportError as e:
        articles = None
        # Handle ImportError if models.py is not found or has issues
        print(f"❌ Error fetching report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# Route the Analysis page
@app.route("/api/analysis", methods=["GET"])
def analysis() -> tuple:
    """Function returning a json response for the analysis page."""
    # Build a welcome message displaying the app name
    welcome_message = "👨‍💻⚒️ Welcome to CyberMag Analysis page!"
    count = 9

    try:
        # Assuming this function returns analysis data
        articles_analysis = get_all_site()

        # if not articles_analysis "analysis" is empty
        if not articles_analysis:
            welcome_message += " No analysis found."
        else:
            welcome_message += f"Latest {count} Analisys of Cyber Attacks:"

        articles_data = []
        for article in articles_analysis[:count]:
            try:
                analysis_item = {
                    "site_name": article.get("site_name"),
                    "title": article.get("title", "No Title"),
                    "summary": article.get("summary", "No Summary"),
                    "risk_level": article.get("risk_level", "Unknown"),
                }
                articles_data.append(analysis_item)
            except (KeyError, TypeError) as e:
                print(f"❌ Error processing article: {e}")
                continue

        # Return the welcome message as a JSON response with 200 status code
        return (
            jsonify(
                {
                    "success": True,
                    "message": welcome_message,
                    # return only title, summary, analysis, and risk_level
                    "analysis": articles_data,
                    "count": len(articles_analysis),
                }
            ),
            200,
        )
    except ImportError as e:
        # Handle any exception that might occur when fetching analysis
        error_message = welcome_message + f" ❌ Error fetching analysis: {e}"
        print(f"❌ Error fetching analysis: {e}")
        return (
            jsonify({"success": False, "error": error_message}),
            500,
        )


# Route the About page
@app.route("/about", methods=["GET"])
def about():
    """Function returning a json python version."""
    return jsonify({"message": "👨‍💻⚒️ About page is under construction"})


# Main entry point to run the Flask app
# Uncomment the following line to initialize the database
if __name__ == "__main__":
    # import os

    # print(os.getcwd())

    # from .models2 import init_db, verify_db

    # # Verify if the database is initialized
    # if not verify_db():
    #     print("❌ Database is not initialized.")
    #     # Uncomment ONLY in the first run
    #     init_db()  # Run it once to create Tables
    #     exit(1)

    # Run the Flask apps
    app.run(debug=True, port=5000)

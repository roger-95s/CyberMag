"""Module providing a Flask class and JSON function Python version.
Contains endpoints for CyberMag: home, posts, analysis, and about.
Ensures all articles have consistent IDs and proper icon assignment.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from .models import get_all_site

# Crear Flask app
app = Flask(__name__)
CORS(app)


# Helper para asignar ID y construir artículos
def build_articles(articles_raw, count=None):
    """
    Construye una lista de artículos a partir de la data cruda.
    Asigna un ID incremental si no existe y determina el icono basado en el título.
    """
    articles_data = []
    for idx, article in enumerate(articles_raw[:count] if count else articles_raw, start=1):
        title_lower = article.get("title", "").lower()
        if "ai" in title_lower:
            icon = "ai"
        elif "ransomware" in title_lower:
            icon = "ransomware"
        elif "network" in title_lower:
            icon = "network"
        elif "threat" in title_lower:
            icon = "threats"
        elif "global" in title_lower:
            icon = "globe"
        else:
            icon = "unknown"

        articles_data.append({
            "id": article.get("id") or idx,
            "title": article.get("title", "No Title"),
            "summary": article.get("summary", "No Summary"),
            "analysis": article.get("analysis", "No Analysis"),
            "risk_level": article.get("risk_level", "Unknown"),
            "url": article.get("url", "No Urls"),
            "site_name": article.get("site_name", "No Site Name"),
            "icon": icon,
            "date": article.get("date")
        })
    return articles_data


# Endpoint /api/home
@app.route("/api/home", methods=["GET", "POST"])
def home():
    """Home route returning a welcome message and 9 articles."""
    try:
        articles_raw = get_all_site()
        count = 9
        articles = build_articles(articles_raw, count)
        welcome_message = (
            "👨‍💻⚒️ Welcome to CyberMag! "
            "This is an app for managing cybersecurity reports. "
            "Use the /post endpoint or click on a report to see more."
        )
        if articles:
            welcome_message += f" Latest {len(articles)} Articles of Cyber Attacks:"
        else:
            welcome_message += " No articles found."

        return jsonify({"success": True, "message": welcome_message, "articles_data": articles}), 200
    except Exception as e:
        print(f"❌ Error in /api/home: {e}")
        return jsonify({"success": False, "error": str(e), "articles_data": []}), 500


# Endpoint /api/post (todos los artículos)
@app.route("/api/post", methods=["GET"])
def post_reports():
    """Returns all articles with count and details."""
    try:
        articles_raw = get_all_site()
        articles = build_articles(articles_raw)
        return jsonify({"success": True, "count": len(articles), "articles": articles}), 200
    except Exception as e:
        print(f"❌ Error in /api/post: {e}")
        return jsonify({"success": False, "error": str(e), "articles": []}), 500


# Endpoint /api/post/<post_id> (artículo individual)
@app.route("/api/post/<int:post_id>", methods=["GET"])
def get_single_report(post_id):
    """
    Returns a single article by ID.
    If not found, returns 404 with error message.
    """
    try:
        articles_raw = get_all_site()
        articles = build_articles(articles_raw)
        article = next((a for a in articles if a["id"] == post_id), None)
        if article:
            return jsonify({"success": True, "article": article}), 200
        return jsonify({"success": False, "error": "Article not found"}), 404
    except Exception as e:
        print(f"❌ Error in /api/post/<post_id>: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# Endpoint /api/analysis
@app.route("/api/analysis", methods=["GET"])
def analysis():
    """
    Returns latest 9 articles with full analysis details.
    Only includes title, summary, analysis, risk level, and other info.
    """
    try:
        articles_raw = get_all_site()
        count = 9
        articles = build_articles(articles_raw, count)
        return jsonify({
            "success": True,
            "message": f"👨‍💻⚒️ Latest {len(articles)} Analysis of Cyber Attacks",
            "analysis": articles,
            "count": len(articles)
        }), 200
    except Exception as e:
        print(f"❌ Error in /api/analysis: {e}")
        return jsonify({"success": False, "error": str(e), "analysis": []}), 500


# Endpoint /about
@app.route("/about", methods=["GET"])
def about():
    """Returns about page message."""
    return jsonify({"message": "👨‍💻⚒️ About page is under construction"})


if __name__ == "__main__":
    # Main entry point to run the Flask app
    app.run(debug=True, port=5000)

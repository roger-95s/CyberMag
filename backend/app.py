from flask import Flask, jsonify, render_template
from flask_cors import CORS
from .scraper import fetch_data
from .models import get_all_reports, save_report, init_db


# Create Flask app
app = Flask(__name__)
CORS(app)


# Api router: fetch and analyze latest cyber news
@app.route("/api/index", methods=["GET", "POST"])
def index(): 
    return jsonify({
        "message ":"👨‍💻⚒️ We're Working soon you will be able to see the result"
        })

# API route: return all stored reports 
@app.route("/api/reports", methods=["GET"])
def get_reports():
    try:
        articles = get_all_reports()
        return jsonify({
            "success": True,
            "count": len(articles),
            "articles": articles
        })
    except Exception as e:
        return ({
            "success": False,
            "error": str(e),
            "articles": []
        }), 500

"""
# Optional: Add a route to get a single report by ID
@app.route("/api/reports/<int:report_id>", methods=["GET"])
def get_single_report(report_id):
    try:
        articles = get_all_reports()
        article = next((a for a in articles if a["id"] == report_id), None)
        if article:
            return jsonify({
                "success": True,
                "article": article
            })
        else:
            return jsonify({
                "success": False,
                "error": "Article not found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
"""

if __name__ == "__main__":
    # init_db() # Run it one to create the DataBase?
    app.run(debug=True, port=5000)
"""Module providing a flaks class and json function python version."""

from flask import Flask, jsonify
from flask_cors import CORS
from .models import get_all_reports


# Create Flask app
app = Flask(__name__)
CORS(app)


# Api router: fetch and analyze latest cyber news
@app.route("/api/index", methods=["GET", "POST"])
def index():
    """Function returning a json python version."""
    return jsonify({"message ": "👨‍💻⚒️ Website's being build"})


# API route: return all stored reports
@app.route("/api/reports", methods=["GET", "POST"])
def get_reports():
    """Function get_reports return json python version."""
    try:
        articles = get_all_reports()
        return (
            jsonify({"success": True, "count": len(articles), "articles": articles}),
            200,
        )
    except ImportError as e:
        return ({"success": False, "error": str(e), "articles": []}), 500


# Uncomment the following lines if you want to add a route to save reports"
# Optional: Add a route to get a single report by ID
@app.route("/api/reports/<int:report_id>", methods=["GET"])
def get_single_report(report_id):
    try:
        from .models import get_all_reports  # Import here to avoid circular import

        articles = get_all_reports()
        article = next((a for a in articles if a["id"] == report_id), None)
        if article:
            return jsonify({"success": True, "article": article})
        return jsonify({"success": False, "error": "Article not found"}), 404
    except ImportError as e:
        articles = None
        # Handle ImportError if models.py is not found or has issues
        print(f"❌ Error fetching report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    # init_db()  # Run it one to create the DataBase?
    app.run(debug=True, port=5000)

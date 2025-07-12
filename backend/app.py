"""Module providing a flaks class and json function python version."""

from flask import Flask, jsonify
from flask_cors import CORS
from .models import get_all_reports


# Create Flask app
app = Flask(__name__)
CORS(app)


# Route to get all reports
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


# Route the Analysis page
@app.route("/api/analysis", methods=["GET"])
def analysis():
    """Function returning a json python version."""
    return jsonify({"message": "👨‍💻⚒️ Analysis page is under construction"})


# Route the About page
@app.route("/api/about", methods=["GET"])
def about():
    """Function returning a json python version."""
    return jsonify({"message": "👨‍💻⚒️ About page is under construction"})


# Main entry point
@app.route("/", methods=["GET"])
def home():
    """Function returning a json python version."""
    return jsonify({"message": "👨‍💻⚒️ Welcome to CyberMag!"})


if __name__ == "__main__":
    # init_db()  # Run it one to create the DataBase?
    app.run(debug=True, port=5000)

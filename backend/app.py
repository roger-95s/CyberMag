"""Module providing a flaks class and json function python version."""

from flask import Flask, jsonify
from flask_cors import CORS
from .models import init_db, get_all_reports


# Create Flask app
app = Flask(__name__)
CORS(app)


# Route the home page
@app.route("/", methods=["POST", "GET"])
def home() -> tuple:
    """Home route returning a welcome message and 9 articles."""
    # Build a welcome message displaying the app name
    welcome_message = "👨‍💻⚒️ Welcome to CyberMag!   "
    welcome_message += "... This is a App for managing cyber security reports.  "
    welcome_message += (
        "... Use the /post or click on resport to see moro endpoint to view reports.  "
    )
    # Try to display the first 9 articles in the welcome message
    count = 9
    articles = get_all_reports()
    try:
        if not articles:
            welcome_message += " No reports found."
        else:
            welcome_message += f"Latest {count} Cyber Attacks:"

            if len(articles) > count:
                # For more articles, add a button or link to view all posts reports
                welcome_message += (
                    f"\n... and {len(articles) - count} more. Click here for more."
                )

        # Return the welcome message as a JSON response with 200 status code
        return (
            jsonify(
                {
                    "success": True,
                    "message": welcome_message,
                    "articles": articles[:count],
                }
            ),
            200,
        )
    # Handle ImportError if models.py is not found or has issues
    except ImportError as e:
        welcome_message += f" ❌ Error fetching reports: {e}", 500
        return (
            jsonify({"success": False, "error": str(e), "message": welcome_message}),
            500,
        )


# Route to get all reports
@app.route("/post", methods=["GET", "POST"])
def post_reports():
    """Function post_reports return True if successful,
    len(articles) and articles, and A list of articles."""
    # try to get all reports from the database
    try:
        articles = get_all_reports()
        return (
            jsonify({"success": True, "count": len(articles), "articles": articles}),
            200,
        )
    # Handle ImportError if models.py is not found or has issues
    except ImportError as e:
        return ({"success": False, "error": str(e), "articles": []}), 500


# Uncomment the following lines if you want to add a route to save reports"
# Optional: Add a route to get a single report by ID
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def get_single_report(post_id):
    try:
        from .models import get_all_reports  # Import here to avoid circular import

        articles = get_all_reports()
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
@app.route("/analysis", methods=["GET", "POST"])
def analysis() -> tuple:
    """Function returning a json response for the analysis page."""
    # Build a welcome message displaying the app name
    welcome_message = "👨‍💻⚒️ Welcome to CyberMag Analysis page!"
    count = 9

    try:
        # Assuming this function returns analysis data
        articles_analysis = get_all_reports()

        # if not articles_analysis "analysis" is empty
        if not articles_analysis:
            welcome_message += " No analysis found."
        else:
            welcome_message += f"Latest {count} Analisys of Cyber Attacks:"

        articles_data = []
        for article in articles_analysis[:count]:
            try:
                analysis_item = {
                    "title": article.get("title", "No Title"),
                    "analysis": article.get("analysis", "No Analysis"),
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
                    # return only title, analysis, and risk_level
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
    init_db()  # Run it one to create the DataBase?
    app.run(debug=True, port=5000)

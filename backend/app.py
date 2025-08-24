"""Module providing a flaks class and json function python version."""

from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.models import get_all_reports, save_report



# Create Flask app
app = Flask(__name__)
CORS(app)


# Route the home page
@app.route("/api/index", methods=["POST", "GET"])
def home() -> tuple:
    """Home route returning a welcome message and 9 articles."""

    # Build a welcome message displaying the app name
    welcome_message = (
        "👨‍💻⚒️ Welcome to CyberMag! "
        "This is an app for managing cybersecurity reports. "
        "Use the /post endpoint or click on a report to see more."
    )
    # Try to display the first 9 articles in the welcome message
    count = 9

    try:
        # Get all reports from the database
        articles = get_all_reports()
        # if not articles list is empty
        if not articles:
            welcome_message += " No articles found."
        else:
            welcome_message += f" Latest {count} Articles of Cyber Attacks:"

        articles_data = []
        for article in articles[:count]:
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
                    "id": article.get("id"),
                    "title": article.get("title", "No Title"),
                    "url": article.get("url", "No Urls"),
                    "summary": article.get("summary", "No Summary"),
                    "risk_level": article.get("risk_level", "Unknown"),
                    "icon": icon,
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
                }
            ),
            200,
        )
    except Exception as e:
        # Handle any exception that might occur when fetching analysis
        error_message = welcome_message + f" ❌ Error: {e}"
        print(f"❌ Error fetching analysis: {e}")
        return (
            jsonify({"success": False, "error": error_message}),
            500,
        )


# Route to get all reports
@app.route("/post", methods=["GET"])
def post_reports():
    """Function post_reports return True if successful,
    len(articles) and articles, and A list of articles."""

    try:
        articles = get_all_reports()
        return (
            jsonify({"success": True, "count": len(articles), "articles": articles}),
            200,
        )
    except Exception as e:
        return ({"success": False, "error": str(e), "articles": []}), 500


# Route to save a new report manually
@app.route("/post", methods=["POST"])
def create_report():
    """Function to save a new report via POST request.
    Needs: title, url, summary, risk_level
    """
    try:
        data = request.json
        save_report(data)
        return jsonify({"success": True, "message": "✅ Report saved"}), 201
    except Exception as e:
        print(f"❌ Error creating report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# Optional: Add a route to get a single report by ID
@app.route("/post/<int:post_id>", methods=["GET"])
def get_single_report(post_id):
    try:
        articles = get_all_reports()
        article = next((a for a in articles if a["id"] == post_id), None)
        if article:
            return jsonify({"success": True, "article": article})
        # Return 404 if article not found
        return jsonify({"success": False, "error": "Article not found"}), 404
    except Exception as e:
        print(f"❌ Error fetching report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# Route the Analysis page
@app.route("/analysis", methods=["GET"])
def analysis() -> tuple:
    """Function returning a json response for the analysis page."""

    welcome_message = "👨‍💻⚒️ Welcome to CyberMag Analysis page!"
    count = 9

    try:
        # Get all reports
        articles_analysis = get_all_reports()

        # if not articles_analysis is empty
        if not articles_analysis:
            welcome_message += " No analysis found."
        else:
            welcome_message += f" Latest {count} Analysis of Cyber Attacks:"

        articles_data = []
        for article in articles_analysis[:count]:
            try:
                analysis_item = {
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
                    # return only title, summary, and risk_level
                    "analysis": articles_data,
                    "count": len(articles_analysis),
                }
            ),
            200,
        )
    except Exception as e:
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
if __name__ == "__main__":
    app.run(debug=True, port=5000)

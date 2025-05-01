from flask import Flask, jsonify
from flask_cors import CORS
from .models import get_all_reports, save_report
from .scraper import fetch_latest_articles
from .llm_tools import analyze_article

# print(fetch_latest_articles())

# Create Flask app
app = Flask(__name__)
CORS(app)

#  Api router: fetch and analyze latest cyber news
@app.route("/api/new", methods=["GET"])
def get_news():
    """
    Fetch latest cyber news and analyze using LLM.
    """
    print("🔍 Called /api/new route")

    # Fetch latest articles 
    articles = fetch_latest_articles()

    reports = []

    # process each article 
    for article in articles:
        try:
            #  First analyze  the article
            report = analyze_article(article) 
            print(f"🤞{report}")
            reports.append(report)
            
            # Call save_report for each article
            saved_reports_db = save_report(report_data=report)
            print(f"🎲 {saved_reports_db}")

        except Exception as e:
            print(f"❌ New_report exption error: {e}")

    return reports



# API route: return all stored reports 
@app.route("/api/reports", methods=["GET"])
def get_reports():

    article = get_all_reports()
    return jsonify(article)

if __name__ == "__main__":
    # init_db() # Run it one to create the DataBase?
    app.run(debug=True, port=5001)

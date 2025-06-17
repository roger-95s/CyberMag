from flask import Flask, jsonify, render_template
from flask_cors import CORS
from .scraper import fetch_data
from .models import get_all_reports, save_report


# Create Flask app
app = Flask(__name__)
CORS(app)


# Api router: fetch and analyze latest cyber news
@app.route("/api/index", methods=["GET", "POST"])
def index(): 
    return jsonify(f"👨‍💻⚒️ We're Working soon you will be able to see the result")

# API route: return all stored reports 
@app.route("/api/reports", methods=["GET"])
def get_reports():

    article = get_all_reports()
    return jsonify(article)

if __name__ == "__main__":
    # init_db() # Run it one to create the DataBase?
    app.run(debug=True, port=5000)
from flask import Flask, jsonify
from flask_cors import CORS
from .models import get_all_reports, save_report
from .scraper import scraper

# Create Flask app
app = Flask(__name__)
CORS(app)


#  Api router: fetch and analyze latest cyber news
@app.route("/api/new", methods=["GET"])
def get_news():
    
    return scraper()
    
   

# API route: return all stored reports 
@app.route("/api/reports", methods=["GET"])
def get_reports():

    article = get_all_reports()
    return jsonify(article)

if __name__ == "__main__":
    # init_db() # Run it one to create the DataBase?
    app.run(debug=True, port=5001)

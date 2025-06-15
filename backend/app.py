from flask import Flask, jsonify
from flask_cors import CORS
from .scraper import extract_data, articles
from .models import get_all_reports, save_report


# Create Flask app
app = Flask(__name__)
CORS(app)


# Api router: fetch and analyze latest cyber news
@app.route("/api/rawdata", methods=["GET"])
def rawdata():  
    """
        Display data that was just extracted and return it. 
        Into a dict_list or a json
    """ 
    # Pass raw data extracted from extrac_data()
    data = []

    if data:
        try:
            data.append(articles)
            print(f"✅ Data was passed successful: {data}")

            return jsonify(data['name'])
        except Exception as e:
            print(f"❌ Error during opperation: {e}")
    else:
        return jsonify(f"👨‍💻⚒️ We're Working soon you will be able to see the result")

# API route: return all stored reports 
@app.route("/api/reports", methods=["GET"])
def get_reports():

    article = get_all_reports()
    return jsonify(article)

if __name__ == "__main__":
    # init_db() # Run it one to create the DataBase?
    app.run(debug=True, port=5000)
"""Module providing a flaks class and json function python version."""
from flaskr import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    
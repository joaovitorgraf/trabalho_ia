from flask import Flask
from flask_cors import CORS
from src.Routes.routes import routes

app = Flask(__name__, static_url_path="/media", static_folder="media")
CORS(app)
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)

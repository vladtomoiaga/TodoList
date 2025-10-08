import os
from dotenv import load_dotenv
from flask import Flask
from routes import routes

def create_app():
    app = Flask(__name__)

    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    app.config['SECRET_KEY'] = SECRET_KEY

    app.register_blueprint(routes)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

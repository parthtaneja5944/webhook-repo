from flask import Flask
from app.extensions import db
from app.webhook.routes import webhook
import os

def create_app():

    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/webhook_db"
    db.init_app(app)
    app.register_blueprint(webhook)
   
    return app

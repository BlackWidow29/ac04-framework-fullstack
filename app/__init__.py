# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .controller.rotas import app

# app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
db = SQLAlchemy(app)

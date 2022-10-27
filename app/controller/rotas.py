# from app import app, db
from flask import Flask, make_response, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def root():
    return "<h1>Ac04 de Fullstack</h1>" 
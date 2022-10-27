# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .controller.rotas import app
from .controller import rotas
from flask_restful import Resource, Api

api = Api(app)
app.config.from_object('config')
db = SQLAlchemy(app)

api.add_resource(rotas.Contrato, '/contrato/<string:numero_contrato>/')
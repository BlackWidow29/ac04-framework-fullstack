# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .controller.rotas import app
from .controller import rotas
from flask_restful import Resource, Api

api = Api(app)
app.config.from_object('config')
db = SQLAlchemy(app)

api.add_resource(rotas.Contrato, '/contrato/<string:numero_contrato>/')
api.add_resource(rotas.AllContratos, '/contrato/')

api.add_resource(rotas.Cliente,'/cliente/<string:cliente_id>/')
api.add_resource(rotas.AllClientes,"/cliente/")

api.add_resource(rotas.Telefone,'/telefone/<string:telefone_id>/')
api.add_resource(rotas.AllTelefone,"/telefone/")

api.add_resource(rotas.UF,'/Uf/<string:uf_id>/')
api.add_resource(rotas.AllUF,"/uf/")

api.add_resource(rotas.Endereco,'/Endereco/<string:cliente_id>/<string:endereco_id>/')
api.add_resource(rotas.AllEndereco,"/Endereco/")
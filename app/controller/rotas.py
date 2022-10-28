from inspect import Attribute
from urllib import response
from flask import request, jsonify, Flask
from flask_restful import Resource
from ..model import Tables

app = Flask(__name__)


class Contrato(Resource):
    def get(delf, numero_contrato):
        contrato = Tables.Contrato.query.filter_by(
            numero_contrato=numero_contrato).first()
        parcelas = Tables.Parcelas.query.filter(
            Tables.Parcelas.contrato_id == numero_contrato)
        cliente = Tables.Cliente.query.filter_by(
            Tables.Cliente.id == contrato.cliente_id)

        try:
            response = {
                'numero_contrato': contrato.numero_contrato,
                'saldo_devedor': contrato.saldo_devedor,
                'saldo_total': contrato.saldo_total,
                'taxa': contrato.taxa,
                'situacao_contrato': contrato.situacao_contrato,
                'parcelas': [
                    {
                        'numero_parcela': parcela.numero_parcela,
                        'valor_parcela': parcela.valor_parcela,
                        'situacao_parcela': parcela.situacao_parcela,
                        'data_vencimento_parcela': parcela.data_vencimento_parcela,
                    }
                    for parcela in parcelas
                ],
                'cliente': {
                    'nome': cliente.nome,
                    'sobrenome': cliente.sobrenome
                }
            }
        except AttributeError:
            response = {
                'status': 'error',
                'msg': 'Contrato não encontrado'
            }
        return response


class AllContratos(Resource):
    def post(delf):
        data = request.json
        contrato = Tables.Contrato(numero_contrato=data['numero_contrato'], saldo_devedor=data['saldo_devedor'],
                                   valor_total=data['valor_total'], taxa=data['taxa'],
                                   situacao_contrato=data['situacao_contrato'],
                                   quantidade_parcelas=data['quantidade_parcelas'], cliente_id=data['cliente_id'],
                                   data_contratacao=data['data_contratacao'])

        valor_parcela = data['valor_total'] / data['quantidade_parcelas']
        for i in range(1, data['quantidade_parcelas'] + 1):
            numero_parcela = 1
            parcela = Tables.Parcelas(numero_parcela=numero_parcela, valor_parcela=valor_parcela, situacao_parcela=1,
                                      contrato_id=data['numero_contrato'], contrato=contrato)

            numero_parcela = numero_parcela + 1
            parcela.save()

        contrato.save()


class Telefone(Resource):
    def get(delf, id_telefone):
        telefone = Tables.Telefone.query.filter_by(id=id).first()
        cliente = Tables.Cliente.query.filter_by(
            Tables.Cliente.id == telefone.cliente_id)
        try:
            response = {
                'id': telefone.id,
                'numero': telefone.telefone,
                'principal': telefone.principal,
                'cliente': {
                    'nome': cliente.nome,
                    'sobrenome': cliente.sobrenome
                }
            }
        except AttributeError:
            response = {
                'status': 'error',
                'msg': 'Telefone não encontrado'
            }
        return response


class AllTelefone(Resource):
    def post(delf):
        data = request.json
        telefone = Tables.Telefone(
            id=data['id'], numero=data['numero'], principal=data['principal'], id_cliente=data['id_cliente'])
        telefone.save()

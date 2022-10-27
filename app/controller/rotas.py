from flask import request, jsonify, Flask
from flask_restful import Resource
from ..model import Tables

app = Flask(__name__)


class Contrato(Resource):
    def get(delf, numero_contrato):
        contrato = Tables.Contrato.query.filter_by(numero_contrato=numero_contrato).first()
        parcelas = Tables.Parcelas.query.filter(Tables.Parcelas.contrato_id == numero_contrato)
        cliente = Tables.Cliente.query.filter_by(Tables.Cliente.id == contrato.cliente_id)

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
                'cliente' : {
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

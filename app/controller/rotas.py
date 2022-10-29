from inspect import Attribute
from multiprocessing import Barrier
from urllib import response
from flask import request, jsonify, Flask
from flask_restful import Resource
from ..model import Tables
from ..model.Tables import Cliente

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


class Cliente(Resource):
    def get(delf, cliente_id):
        #cliente = Tables.Cliente.query.filter_by(cliente_id=cliente_id).first()
        cliente = Tables.db_session.query(Tables.Cliente).filter_by(id=cliente_id).first()
        try:
            response = {
                'id': cliente.id,
                'nome': cliente.nome,
                'sobrenome': cliente.sobrenome,
                'agencia': cliente.agencia,
                'conta': cliente.conta,
                'email': cliente.email,
            }
        except AttributeError:
            response = {
                'status': 'error',
                'msg': 'Client não encontrada'
            }
        return response

    def put(delf, cliente_id):
        cliente = Tables.Cliente.query.filter_by(
            cliente_id=cliente_id).first()
        data = request.json
        if 'nome' in data:
            cliente.cliente_id = data['nome']
        if 'sobrenome' in data:
            cliente.sobrenome = data['sobrenome']
        if 'agencia' in data:
            cliente.agencia = data['agencia']
        if 'conta' in data:
            cliente.conta = data['conta']
        if 'email' in data:
            cliente.email = data['email']

        cliente.save()
        response = {
                'id': cliente.id,
                'nome': cliente.nome,
                'sobrenome': cliente.sobrenome,
                'agencia': cliente.agencia,
                'conta': cliente.conta,
                'email': cliente.email,
        }
        return response


    def delete(self, cliente_id):
        try:
            cliente = Tables.db_session.query(Tables.Cliente).filter_by(id=cliente_id).first()
            status = 'success'
            msg = 'Cliente {} inativado com sucesso'.format(Tables.Cliente.delete(cliente))
        except AttributeError:
            status = 'error'
            msg = 'Cliente com o id {} não encontrado'.format(cliente_id)
        return jsonify({'status': status, 'mensagem': msg})

class AllClientes(Resource):
    def get(delf):
        clientes = Tables.db_session.query(Tables.Cliente).all()
        response = [{'id': i.id, 'nome': i.nome, 'sobrenome': i.sobrenome,
                     'agencia': i.agencia, 'conta': i.conta, 'email': i.email} for i in clientes]
        return jsonify(response)

    def post(delf):
        data = request.json
        cliente = Tables.Cliente(
            nome=data['nome'], sobrenome=data['sobrenome'], agencia=data['agencia'], conta=data['conta'], email=data['email'])
        cliente.save()
        response = {
                'id': cliente.id,
                'nome': cliente.nome,
                'sobrenome': cliente.sobrenome,
                'agencia': cliente.agencia,
                'conta': cliente.conta,
                'email': cliente.email,
        }
        return response


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


class UF(Resource):
    def get(delf, id_uf):

        id = Tables.Uf.query.filter_by(id=id).first()
        uf = Tables.Uf.query.filter_by(id=id)
        
        try:
            response = {
                'id': id,
                'uf': uf
            }
        except AttributeError:
            response = {
                'status': 'error',
                'msg': 'UF não encontrado.'
            }
        return response
        
class AllUF(Resource):
    def get(delf):
        data = request.json
        uf = Tables.Uf(
            id=data['id'], uf=data['uf'])
        uf.save() 
        return response


class Endereco(Resource):
    def get(delf, cliente_id, endereco_id):
        endereco = Tables.Endereco.query.filter_by(id = endereco_id).first()
        cliente = Tables.Cliente.query.filter_by(
            Tables.Cliente.id == cliente_id)
        Uf = Tables.Uf.query.filter(
            Tables.Uf.id == Uf)
        try:
            response = {
                'id': endereco.id,
                'cliente_id': cliente.id,
                'cep': endereco.cep,
                'logradouro': endereco.logradouro,
                'bairro': endereco.bairro,
                'numero': endereco.numero,
                'cidade': endereco.cidade,
                'complemento': endereco.complemento,
                'uf': [
                    {
                        'id': Uf.id,
                        'uf': Uf.uf
                    }
                ]
            }
        except AttributeError:
            response = {
                'status': 'error',
                'msg': 'Endereço não encontrada'
            }
        return response

    def put(delf, cliente_id, endereco_id):
        cliente = Tables.Cliente.query.filter_by(
            cliente_id=cliente_id).first()
        endereco = Tables.Endereco.query.filter_by(
            endereco_id = endereco_id).first()
        data = request.json

        if 'cep' in data:
            endereco.cep = data['cep']
        if 'logradouro' in data:
            endereco.logradouro = data['logradouro']    
        if 'bairro' in data:
            endereco.bairro = data['bairro']
        if 'numero' in data:
            endereco.numero = data['numero']
        if 'cidade' in data:
            endereco.cidade = data['cidade']
        if 'complemento' in data:
            endereco.complemento = data['complemento']
 
        endereco.save()
        response = {
                'id': endereco.id,
                'cep': endereco.cep,
                'logradouro': endereco.logradouro,
                'bairro': endereco.bairro,
                'numero': endereco.numero,
                'cidade': endereco.cidade,
                'complemento': endereco.complemento,
        }
        return response
 
    def delete(self, endereco_id):
        try:
            endereco = Tables.Endereco.query.filter_by(
                endereco_id = endereco_id).first()
            status = 'success'
            msg = 'Endereço {} removido com sucesso'.format(
                endereco.id)
            endereco.delete()
        except AttributeError:
            status = 'error'
            msg = 'Endereço com o id {} não encontrado'.format(endereco)
        return jsonify({'status': status, 'mensagem': msg})
        
class AllEndereco(Resource):
    def get(delf):
        data = request.json
        endereco = Tables.Endereco(
            id=data['id'], cep=data['cep'],
            logradouro=data['logradouro'], bairro=data['bairro'],
            numero=data['numero'], cidade=data['cidade'],
            complmeneto=data['complmeneto']
        )
        endereco.save() 
        return response
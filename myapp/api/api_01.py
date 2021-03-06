from myapp import db
from myapp.api.schemas.serializers import pedido_schema, pedidos_schema, status_schema, ticket_schema
from myapp.celery import session, async_request ,create_request_credit
from flask_restx import Namespace, Resource, fields, Api
from flask import jsonify, request, json, sessions
from myapp.models import CreditRequest, db

ns = Namespace('credito', description='API - PARA PEDIDO DE CRÉDITO E ACOMPANHAMENTO DO STATUS DO PEDIDO')

pedido_credito = ns.model(
    'JSON para pedido de crédito', {
        'nome': fields.String(
            description='Nome do usuário',
            required=True,
            min_length=4
        ),
        'idade': fields.Integer(
            required=True,
            description='idade do usuário',
        ),     
        'valor_solicitado': fields.Float(
            description='Valor solicitado, deve ser menor que R$ 100.000,00',
            required=True
        ),
        'CPF': fields.String(
            description='CPF do usuário',
            required=True
        )
    }
)
resposta_response_credito = ns.model(
    'Status do pedido', {
        'id': fields.String(
            required=True,
            description='ticket do pedido para acompanhamento'
        ),
        'status': fields.String(
            required=True,
            description='Status do pedido'
        ),
        'resultado_validacao_proposta': fields.String(
            required=True,
            description='resultado possiveis: proposta aprovada, rejeitada ou null'
        ),
        'resultado_validacao_regras': fields.String(
            required=True,
            description=''
        ),
        'ticket do pedido': fields.String(
            required=True,
            description='ticket gerado para consulta do status do pedido'
        )
    }
)

@ns.route('/<ticket>') 
@ns.doc(params={'ticket': 'ID do pedido'})
class ConsultaStatusCredito(Resource):
    def get(self, ticket):
        ticket = CreditRequest.query.filter_by(ticket=ticket).first()
        return status_schema.dump(ticket)
        

@ns.route('/', doc={"description": 'Cria uma solicitação de crédito'})
class SolicitaPedidoCredito(Resource):
    @ns.expect(pedido_credito, validate=True)
    def post(self):      
        try:
            data = request.get_json()
            # create_request_credit(data=data)
            async_request.apply_async(args=[data], countdown=5)
            return "ok"
        except Exception as error:
            print(error)
        finally:
            return jsonify(f"Pedido enviado, consulte o status com o ticket")
# @ns.route('/consulta', doc={"description": 'consulta todas as solicitações de crédito'})   
# @ns.param('consulta', 'consulta tudo')   
# class ConsultaAllPedidos(Resource):
#     def get(self):
#         pedidos = CreditRequest.query.all()
#         return pedidos_schema.dump(pedidos)


def ns_api(api):
    api.add_namespace(ns)
    return None

from myapp import db
from myapp.celery import  async_request, Querys
from flask_restx import Namespace, Resource, fields, Api
from flask import jsonify, request, json, sessions
from myapp.models import CreditRequest, db
import uuid
from .schemas.serializers import ns, resposta_response_credito, pedido_credito

@ns.route('/<ticket>') 
@ns.doc(params={'ticket': 'ID do pedido'})
class ConsultaStatusCredito(Resource):
    # @ns.expect(ticket_consulta)
    def get(self, ticket):
        ticket = CreditRequest.query.filter_by(ticket=ticket).first()

        if not ticket:
            return ({"message": 'ticket nao encontrado!'}) 

        ticket_data = {}
        ticket_data['nome'] = ticket.nome
        ticket_data['ticket'] = ticket.ticket
        ticket_data['idade'] = ticket.idade
        ticket_data['status'] = ticket.status
        ticket_data['valor_solicitado'] = ticket.valor_solicitado    
        return jsonify({"status": ticket_data})   
        

@ns.route('/', doc={"description": 'Cria uma solicitação de crédito'})
class SolicitaPedidoCredito(Resource):
    @ns.expect(pedido_credito, validate=True)
    def post(self):
        session = db.session
        try:
            data = request.get_json()
            Querys.create_request(session, data=data)
            async_request.apply_async(args=[data], countdown=3)
            session.commit()
            return "Pedido enviado!"
        except Exception as error:
            print(error)
        return jsonify({"message": 'sucesso'})


# @ns.route('/consulta', doc={"description": 'consulta todas as solicitações de crédito'})   
# @ns.param('consulta', 'consulta tudo')   
# class ConsultaAllPedidos(Resource):
#     # @ns.expect(resposta_response_credito)
#     def get(self):
#         pedidos = CreditRequest.query.all()
#         output = []
#         for pedido in pedidos:
#             pedido_data = {}
#             pedido_data['nome'] = pedido.nome
#             pedido_data['idade'] = pedido.idade
#             pedido_data['valor_solicitado'] = pedido.valor_solicitado
#             pedido_data['ticket'] = pedido.ticket
#             output.append(pedido_data)
#         return jsonify({"pedido": output})


# #endpoint de teste
# @ns.route('/process/<name>')
# class Teste(Resource):
#     def get(self, name):
#         reverse.delay(name)

#         return " i sent async" 

# registrando recursos do ns para a instancia de API

def ns_api(api):
    api.add_namespace(ns)
    return None

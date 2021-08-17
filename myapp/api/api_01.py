from flaskapp import db
from flask_restx import Namespace, Resource, fields, Api
from flask import jsonify, request
from flaskapp.models import CreditRequest, db
import uuid

ns = Namespace('credito', description='REST API - SOLICITAÇÃO DE CRÉDITO')

# fields for object serialization
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
        )
    }
)
# fields for object serialization
recebe_response_credito = ns.model(
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
        )
    }
)
# fields for object serialization
ticket_consulta = ns.model(
    'Ticket do pedido', {
        'ticket': fields.String(
            required=True,
            description='ticket gerado em formato de UUID4'
        )
    }
)


@ns.route('/<ticket>', doc={"description": 'Verifica status da solicitação de cŕedito'})
@ns.param('ticket', 'ticket do pedido')
class ConsultaStatusCredito(Resource):
    @ns.expect(ticket_consulta)
    def get(self, ticket):
        ticket = CreditRequest.query.filter_by(ticket=ticket).first()

        if not ticket:
            return ({"message": 'ticket nao encontrado!'}) 

        ticket_data = {}
        ticket_data['nome'] = ticket.nome
        ticket_data['idade'] = ticket.idade
        ticket_data['status'] = ticket.status
        ticket_data['valor_solicitado'] = ticket.valor_solicitado    
        return jsonify({"status": ticket_data})   
        

@ns.route('/consulta', doc={"description": 'consulta todas as solicitações de crédito'})   
@ns.param('consulta', 'consulta tudo')   
class ConsultaAllPedidos(Resource):
    def get(self):
        pedidos = CreditRequest.query.all()
        output = []

        for pedido in pedidos:
            pedido_data = {}
            pedido_data['nome'] = pedido.nome
            pedido_data['idade'] = pedido.idade
            pedido_data['valor_solicitado'] = pedido.valor_solicitado
            pedido_data['ticket'] = pedido.ticket
            output.append(pedido_data)
        return jsonify({"pedido": output})


@ns.route('/', doc={"description": 'Cria uma solicitação de crédito'})
class SolicitaPedidoCredito(Resource):
    @ns.expect(pedido_credito, validate=True)
    def post(self):
        data = request.get_json()
        
        if data == {}:
            return jsonify({"error": "error"}), 204
        elif data['idade'] < 18 or data['valor_solicitado'] > 1001:
            novo_pedido = CreditRequest(ticket=str(uuid.uuid4()), nome=data['nome'], idade=data['idade'] , valor_solicitado=data['valor_solicitado'], status='None')
            db.session.add(novo_pedido)
            db.session.commit()

            return jsonify({"message": 'pedido de credito nao aprovado!'}, {"message2":  'não foi possivel processar o pedido!'})
        else:
            novo_pedido = CreditRequest(ticket=str(uuid.uuid4()), nome=data['nome'], idade=data['idade'] , valor_solicitado=data['valor_solicitado'], status='aprovado!')
            # task = create_task.delay(int(novo_pedido))
            db.session.add(novo_pedido)
            db.session.commit()
    
            print("Não foi possivel processar o pedido!")   

        return jsonify({"message": "request enviado! "})



# vinculando o namespace a API restx
def ns_api(api: Api):
    api.add_namespace(ns)
    return None
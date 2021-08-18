from myapp import celery, db
import logging
from .models import CreditRequest
import uuid
from flask import jsonify

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

def create_request(session, data):
    novo_pedido = CreditRequest(ticket=str(uuid.uuid4()), nome=data['nome'], idade=data['idade'] , valor_solicitado=data['valor_solicitado'], status='Processando')
    session.add(novo_pedido)
    
    return novo_pedido

def consulta_request(session, id):
    return session.query.filter_by(id=id).first()



@celery.task()
def async_request(data):
    session = db.session
    try:
        if data['idade'] < 18 or data['valor_solicitado'] > 100000000:
            novo_pedido = CreditRequest(ticket=str(uuid.uuid4()), nome=data['nome'], idade=data['idade'] , valor_solicitado=data['valor_solicitado'], resultado_validacao_proposta='Reprovado!')
            # consulta_request(session, id)
            session.commit()
            print("Reprovado!")
        else:
            novo_pedido = CreditRequest(ticket=str(uuid.uuid4()), nome=data['nome'], idade=data['idade'] , valor_solicitado=data['valor_solicitado'], resultado_validacao_proposta='Aprovado!')
            # consulta_request(session, id)
            db.session.commit()
            print("Aprovado!")
    except Exception as e:
        print(e)

    return "I sent request"    
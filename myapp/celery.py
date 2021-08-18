from sqlalchemy.orm.query import Query
from myapp import celery, db
import logging
from .models import CreditRequest
import uuid

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

# faltando desenvolvimento aqui

class Querys():
    def create_request(session, data):
        novo_pedido = CreditRequest(ticket=str(uuid.uuid4()),
        nome=data['nome'],
        idade=data['idade'],
        valor_solicitado=data['valor_solicitado'],
        status='Processando')
        session.add(novo_pedido)
        
        return novo_pedido

    def consulta_request(session, _id):
        return session.query.filter_by(id=_id).first()


@celery.task()
def async_request(data):

    # falta desenvolvimento aqui
    session = db.session
    try:
        Querys.consulta_request(session, _id=id)
        if data['idade'] < 18 or data['valor_solicitado'] > 100000000:
            session.query(CreditRequest).filter(CreditRequest.status).update(CreditRequest.status == 'Reprovado!')
            session.commit()
            print("SUcesso")
        else:
            session.query(CreditRequest).filter(CreditRequest.status).update(CreditRequest.status == 'Aprovado!!')
            session.commit()
            print("Sucesso!")
    except Exception as e:
        print(e)

    return "I sent request"    
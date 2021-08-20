from sqlalchemy.orm.query import Query
from myapp import celery, db
import logging
from .models import CreditRequest
import uuid

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:36546655aS!@localhost/teste')
Session = sessionmaker(bind=engine)
session = Session()


class Querys():
    def create_request(data):
        novo_pedido = CreditRequest(ticket=str(uuid.uuid4()),
        nome=data['nome'],
        idade=data['idade'],
        valor_solicitado=data['valor_solicitado'],
        cpf=data['CPF'],
        status='Processando'
        )
        session.add(novo_pedido)
        
        return novo_pedido

    def consulta_request(_id):
        dados = session.query(CreditRequest).filter_by(id=_id).first()
        return dados



@celery.task()
def async_request(data):

    # falta desenvolvimento aqui
    try:
        teste = Querys.consulta_request(id)
        print(teste.id)
        if data['idade'] < 18 or data['valor_solicitado'] > 100000000:
            session.query(CreditRequest).filter(CreditRequest.id == teste._id).update({'status' :'Processado!', "resultado_validacao_pedido": "reprovado!"})
            session.commit()
            print("Reprovado!")
        else:
            session.query(CreditRequest).update({"resultado_validacao_pedido":'Aprovado!!'})
            session.commit()
            print("Sucesso!")
    except Exception as e:
        print(e)

    return "I sent request"    
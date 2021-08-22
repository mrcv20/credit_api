from sqlalchemy.orm.query import Query
from myapp import celery, db
import logging
from .models import CreditRequest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()


engine = create_engine('mysql://root:wasionbr@localhost/teste')
Session = sessionmaker(bind=engine)
session = Session()

def create_request_credit(data):
    try:
        new_reques = CreditRequest(ticket=str(uuid.uuid4()),
        nome=data['nome'],
        idade=data['idade'],
        valor_solicitado=data['valor_solicitado'],
        cpf=data['CPF'],
        status='Processando')
        session.add(new_reques)
        session.flush()
        new_reques.id
    except Exception as error:
        print(error)
    finally:
        mylogger.info(f'ID da sessao atual:{new_reques.id}')
        return new_reques


@celery.task(name="Async Create Request")
def async_request(data):
    try:
        if data['idade'] < 18 or data['valor_solicitado'] > 10000000:
            session.query(CreditRequest).filter(CreditRequest.id == create_request_credit(data).id).\
            update({"status": "Processado", "resultado_validacao_pedido": "Recusado", "resultado_validacao_regras": "Reprovado"})
        else:
            session.query(CreditRequest).filter(CreditRequest.id == create_request_credit(data).id).\
            update({"status": "Processado", "resultado_validacao_pedido": "Aprovado", "resultado_validacao_regras": "Aprovado!"})
    except Exception as e:
        print(e)
    finally:
        mylogger.info(f"Idade do usuário: {data['idade']}, Valor solicitado pelo usuário: {data['valor_solicitado']}\n")
        session.commit()
    return "I sent request"    












# class Querys():
#     def create_request(data):
#         novo_pedido = CreditRequest(ticket=str(uuid.uuid4()),
#         id = id.uuid1(),
#         nome=data['nome'],
#         idade=data['idade'],
#         valor_solicitado=data['valor_solicitado'],
#         cpf=data['CPF'],
#         status='Processando'
#         )
#         session.add(novo_pedido)
#         return novo_pedido
        
#     def update_request(data):
#         novo_pedido = CreditRequest(status=data['status'],
#         resultado_validacao_pedido=data['resultado_validacao_pedido'],
#         resultado_validacao_regras=data['resultado_validacao_regras']
#         )
#         session.add(novo_pedido)
#         return novo_pedido







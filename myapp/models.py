from flask_restx import fields
from myapp import db, ma


class CreditRequest(db.Model):
    __tablename__ = 'credit_request'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    nome = db.Column(
        db.String(64),
        unique=False,
    )
    idade = db.Column(                        
        db.Integer,
        unique=False,
    )      
    valor_solicitado = db.Column(
        db.Float,
        unique=False,
    )
    ticket = db.Column(
        db.String(50),
        unique=True,
    )    
    status = db.Column(
        db.String(20),
        unique=False
    )
    cpf = db.Column(
        db.String(12),
        unique=False
    )
    resultado_validacao_pedido = db.Column(
        db.String(20),
        unique=False
    )
    resultado_validacao_regras = db.Column(
        db.String(20),
        unique=False
    )
    
    def __repr__(self):
        return 'id %d' % self.id

          

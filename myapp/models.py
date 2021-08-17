from myapp import db


class CreditRequest(db.Model):
    __tablename__ = 'credit_request'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    nome = db.Column(
        db.String(64),
        unique=True,
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
    resultado_validacao_proposta = db.Column(
        db.String(20),
        unique=False
    )
    resultado_validacao_regras = db.Column(
        db.String(20),
        unique=False
    )

    def create(self, session, **kwargs):
        new = self.__class__(**kwargs)
        session.add(new)
        return new

    def fetch_data(self, session, id):
        return session.query(self.__class__).filter_by(id=_id).first()

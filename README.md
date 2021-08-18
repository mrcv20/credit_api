
# Rest API

## Sobre

API Rest que recebe pedidos de credito(em testes e desenvolvimento)

Tecnologias:
- Flask
- MySQL
- Redis
- Celery
- Pytest


## System Requirements
  python 3.8, Redis server, MySQL Server


## Instalar Pacotes
```
pip install -r requirements.txt
```

## Ativando ambiente virtual
```
pip install virtualenv

virtualenv {variavel}

source {variavel}/bin/activate
```
## Criação das tabelas e do banco de dados
```
python 
from myapp import create_app, db
app = create_app()
app.app_context().push()
db.create_all()
```

## Subindo a API
```
export FLASK_APP=myapp/run.py
export FLASK_DEBUG=True
flask run
```



- Endereço da documentação: http://localhost:5000/api/v1/

### Comandos de WORKERS e de monitoring com flower
```
celery -A myapp.celery.celery worker --loglevel=info
celery -A myapp.celery.celery flower --port=5566

```
- Endereço do Monitoring com flower http://localhost:5566

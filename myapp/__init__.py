from __future__ import absolute_import
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
import os

db = SQLAlchemy()
# basedir=path.dirname(os.path.realpath(__file__))

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'senhasecretawasion'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:wasionbr@localhost/teste'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

        return app

def make_celery(app):
    celery = Celery(
        'my-app',
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery  

app = create_app()
celery = make_celery(app)

# testando celery
@app.route('/process/<name>')
def process(name):
    reverse.delay(name)

@celery.task()
def reverse(string):
    return string[::-1]    






from flask import Blueprint
from flask_restx import Api
from ..api import api_01

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)
api_01.ns_api(api)


def create_api(app):
    app.register_blueprint(api.blueprint)
    return None
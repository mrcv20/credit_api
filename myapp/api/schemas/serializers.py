from flask_restx import Namespace, Resource, fields, Api
from flask import jsonify, request

ns = Namespace('credito', description='API - PARA PEDIDO DE CRÉDITO E ACOMPANHAMENTO DO STATUS DO PEDIDO')

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
        ),
        'CPF': fields.String(
            description='CPF do usuário',
            required=True
        )
    }
)
resposta_response_credito = ns.model(
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
        ),
        'ticket do pedido': fields.String(
            required=True,
            description='ticket gerado para consulta do status do pedido'
        )
    }
)
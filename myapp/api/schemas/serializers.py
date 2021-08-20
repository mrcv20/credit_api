from myapp import ma


class CreditSchema(ma.Schema):
    class Meta:
        fields = ('nome', 'idade', 'valor_solicitado', 'cpf', 'ticket')

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("detalhe_pedido", values=dict(id="<id>")),
            "collection": ma.URLFor("detalhes")
        }
    )


class StatusSchema(ma.Schema):
    class Meta:
        fields = ("status", "resultado_validacao_pedido", "resultado_validacao_regras")


class ReturnSchema(ma.Schema):
    class Meta:
        fields = ("ticket", "valor_solicitado") 


pedido_schema = CreditSchema()
pedidos_schema = CreditSchema(many=True)
status_schema = StatusSchema()
ticket_schema = ReturnSchema()

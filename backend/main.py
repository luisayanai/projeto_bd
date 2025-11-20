"Camada que gerencia o DB"

from flask import Flask, jsonify
from flask_cors import CORS

# todas as rotas precisam estar registradas aqui no main
from rotas.cliente import cliente_blueprint
from rotas.funcionario import funcionario_blueprint
from rotas.filial import filial_blueprint
from rotas.produto import produto_blueprint
from rotas.fornecedor import fornecedor_blueprint
from rotas.venda import venda_blueprint
from rotas.devolucao import devolucao_blueprint
from rotas.cliente_fidelizado import cliente_fidelizado_blueprint
from rotas.item_venda import item_venda_blueprint
from rotas.pedido import pedido_blueprint
from rotas.relatorios import relatorios_blueprint

# App
app = Flask(__name__)
CORS(app, origins="*")

# root
@app.route("/", methods=["GET"])
def get_root():
    return jsonify("API funcionando"), 200

# registrando as rotas
app.register_blueprint(cliente_blueprint)
app.register_blueprint(funcionario_blueprint)
app.register_blueprint(filial_blueprint)
app.register_blueprint(produto_blueprint)
app.register_blueprint(fornecedor_blueprint)
app.register_blueprint(venda_blueprint)
app.register_blueprint(devolucao_blueprint)
app.register_blueprint(cliente_fidelizado_blueprint)
app.register_blueprint(item_venda_blueprint)
app.register_blueprint(pedido_blueprint)
app.register_blueprint(relatorios_blueprint)

app.run("0.0.0.0", port=8000, debug=False)
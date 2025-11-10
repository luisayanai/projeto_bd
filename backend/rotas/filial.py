#rotas. Recebe as infos via api e chama o servico de filial (servicos/filial.py)

from flask import Blueprint, jsonify, request
from servicos.filial import FilialDatabase

filial_blueprint = Blueprint("filial", __name__)

@filial_blueprint.route("/filial", methods=["GET"])
def get_filiais():
    endereco = request.args.get("endereco", "")
    return jsonify(FilialDatabase().get_filiais(endereco)), 200

@filial_blueprint.route("/filial", methods=["POST"])
def post_filial():
    json = request.get_json()
    endereco = json.get("endereco")
    cpf_gerente = json.get("cpf_gerente")
    telefone = json.get("telefone")

    if not endereco or not cpf_gerente:
        return jsonify("Endereço e CPF do gerente são obrigatórios"), 400

    result = FilialDatabase().cadastra_filial(endereco, cpf_gerente, telefone)
    if result:
        return jsonify("Filial cadastrada"), 200
    return jsonify("Erro ao cadastrar filial"), 400

@filial_blueprint.route("/filial/<endereco>", methods=["PUT"])
def put_filial(endereco):
    json = request.get_json()
    telefone = json.get("telefone")
    cpf_gerente = json.get("cpf_gerente")

    result = FilialDatabase().atualiza_filial(endereco, telefone, cpf_gerente)
    if result:
        return jsonify("Filial atualizada"), 200
    return jsonify("Erro ao atualizar filial"), 400

@filial_blueprint.route("/filial/<endereco>", methods=["DELETE"])
def delete_filial(endereco):
    result = FilialDatabase().deleta_filial(endereco)
    if result:
        return jsonify("Filial deletada"), 200
    return jsonify("Erro ao deletar filial"), 400


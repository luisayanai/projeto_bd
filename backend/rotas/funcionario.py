#rotas. Recebe as infos via api e chama o servico de funcionario (servicos/funcionario.py)

from flask import Blueprint, jsonify, request
from servicos.funcionario import FuncionarioDatabase

funcionario_blueprint = Blueprint("funcionario", __name__)

@funcionario_blueprint.route("/funcionario", methods=["GET"])
def get_funcionarios():
    cpf = request.args.get("cpf", "")
    endereco_filial = request.args.get("endereco_filial", "")
    resultado = FuncionarioDatabase().get_funcionarios(cpf, endereco_filial)
    
    if resultado: return jsonify(resultado), 200
    else: return jsonify('Funcionário não encontrado'), 400

@funcionario_blueprint.route("/funcionario", methods=["POST"])
def post_funcionario():
    json = request.get_json()
    cpf = json.get("cpf")
    nome = json.get("nome")
    salario = json.get("salario")
    endereco_filial = json.get("endereco_filial")
    cpf_supervisor = json.get("cpf_supervisor")

    if not cpf or not nome or salario is None or not endereco_filial:
        return jsonify("CPF, nome, salário e endereço da filial são obrigatórios"), 400

    result = FuncionarioDatabase().cadastra_funcionario(cpf, nome, salario, endereco_filial, cpf_supervisor)
    if result:
        return jsonify("Funcionário cadastrado"), 200
    return jsonify("Erro ao cadastrar funcionário"), 400

# atualizar infos de um funcionário
@funcionario_blueprint.route("/funcionario/<cpf>", methods=["PUT"])
def put_funcionario(cpf):
    json = request.get_json()
    nome = json.get("nome")
    salario = json.get("salario")
    cpf_supervisor = json.get("cpf_supervisor")
    endereco_filial = json.get("endereco_filial")

    result = FuncionarioDatabase().atualiza_funcionario(cpf, nome, salario, cpf_supervisor, endereco_filial)
    if result:
        return jsonify("Funcionário atualizado"), 200
    return jsonify("Erro ao atualizar funcionário"), 400

@funcionario_blueprint.route("/funcionario/<cpf>", methods=["DELETE"])
def delete_funcionario(cpf):
    result = FuncionarioDatabase().deleta_funcionario(cpf)
    if result:
        return jsonify("Funcionário deletado"), 200
    return jsonify("Erro ao deletar funcionário"), 400


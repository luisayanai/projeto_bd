# faz consultas no database para retornar o que precisamos 

from servicos.database.conector import DatabaseManager

class FuncionarioDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider
        
    # funções de controle (queries simples, não vamos mostrar na apresentação)

    def get_funcionarios(self, cpf: str = None, endereco_filial: str = None):
        query = "SELECT * FROM funcionario"
        conditions = []
        if cpf:
            conditions.append(f"cpf = '{cpf}'")
        if endereco_filial:
            conditions.append(f"enderecofilial = '{endereco_filial}'")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        return self.db.execute_select_all(query)

    def get_funcionario_by_cpf(self, cpf: str):
        query = f"SELECT * FROM funcionario WHERE cpf = '{cpf}'"
        return self.db.execute_select_one(query)
    
    def cadastra_funcionario(self, cpf: str, nome: str, salario: float, endereco_filial: str, cpf_supervisor: str = None):
        # ENDEREÇOFILIAL é NOT NULL no schema
        if cpf_supervisor:
            statement = f"INSERT INTO funcionario (cpf, nome, salario, cpfsupervisor, enderecofilial) VALUES ('{cpf}', '{nome}', {salario}, '{cpf_supervisor}', '{endereco_filial}')"
        else:
            statement = f"INSERT INTO funcionario (cpf, nome, salario, enderecofilial) VALUES ('{cpf}', '{nome}', {salario}, '{endereco_filial}')"
        
        return self.db.execute_statement(statement)

    def atualiza_funcionario(self, cpf: str, nome: str = None, salario: float = None, cpf_supervisor: str = None, endereco_filial: str = None):
        updates = []
        if nome:
            updates.append(f"nome = '{nome}'")
        if salario is not None:
            updates.append(f"salario = {salario}")
        if cpf_supervisor:
            updates.append(f"cpfsupervisor = '{cpf_supervisor}'")
        if endereco_filial:
            updates.append(f"enderecofilial = '{endereco_filial}'")
        
        if not updates:
            return False
        
        statement = f"UPDATE funcionario SET {', '.join(updates)} WHERE cpf = '{cpf}'"
        return self.db.execute_statement(statement)

    def deleta_funcionario(self, cpf: str):
        statement = f"DELETE FROM funcionario WHERE cpf = '{cpf}'"
        return self.db.execute_statement(statement)


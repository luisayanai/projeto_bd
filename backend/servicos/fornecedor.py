# faz consultas no database para retornar o que precisamos 

from servicos.database.conector import DatabaseManager

class FornecedorDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider

    # funções de controle (queries simples, não vamos mostrar na apresentação)
    def get_fornecedores(self, cnpj: str = None, nome: str = None):
        query = "SELECT * FROM fornecedor"
        conditions = []
        if cnpj:
            conditions.append(f"cnpj = '{cnpj}'")
        if nome:
            conditions.append(f"nome ILIKE '%{nome}%'")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        return self.db.execute_select_all(query)

    def get_fornecedor_by_cnpj(self, cnpj: str):
        query = f"SELECT * FROM fornecedor WHERE cnpj = '{cnpj}'"
        return self.db.execute_select_one(query)
    
    def cadastra_fornecedor(self, cnpj: str, nome: str, telefone: int | None = None, email: str | None = None):
        if telefone is not None and email:
            statement = f"INSERT INTO fornecedor (cnpj, nome, telefone, email) VALUES ('{cnpj}', '{nome}', {telefone}, '{email}')"
        elif telefone is not None:
            statement = f"INSERT INTO fornecedor (cnpj, nome, telefone) VALUES ('{cnpj}', '{nome}', {telefone})"
        elif email:
            statement = f"INSERT INTO fornecedor (cnpj, nome, email) VALUES ('{cnpj}', '{nome}', '{email}')"
        else:
            statement = f"INSERT INTO fornecedor (cnpj, nome) VALUES ('{cnpj}', '{nome}')"
        
        return self.db.execute_statement(statement)

    def deleta_fornecedor(self, cnpj: str):
        statement = f"DELETE FROM fornecedor WHERE cnpj = '{cnpj}'"
        return self.db.execute_statement(statement)


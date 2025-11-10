# faz consultas no database para retornar o que precisamos 

from servicos.database.conector import DatabaseManager

class FornecedorDatabase():
    def __init__(self, db_provider = DatabaseManager()) -> None:
        self.db = db_provider

    def get_fornecedores(self, cnpj: str = None, id_produto: int = None):
        query = "SELECT * FROM fornecedor"
        conditions = []
        if cnpj:
            conditions.append(f"cnpj = '{cnpj}'")
        if id_produto:
            conditions.append(f"idproduto = {id_produto}")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        return self.db.execute_select_all(query)

    def get_fornecedor_by_cnpj(self, cnpj: str):
        query = f"SELECT * FROM fornecedor WHERE cnpj = '{cnpj}'"
        return self.db.execute_select_one(query)
    
    def cadastra_fornecedor(self, cnpj: str, nome: str, id_produto: int, preco: int, telefone: int = None, email: str = None):
        # IDPRODUTO e PREÇO são NOT NULL no schema
        if telefone and email:
            statement = f"INSERT INTO fornecedor (cnpj, nome, telefone, email, idproduto, preco) VALUES ('{cnpj}', '{nome}', {telefone}, '{email}', {id_produto}, {preco})"
        elif telefone:
            statement = f"INSERT INTO fornecedor (cnpj, nome, telefone, idproduto, preco) VALUES ('{cnpj}', '{nome}', {telefone}, {id_produto}, {preco})"
        elif email:
            statement = f"INSERT INTO fornecedor (cnpj, nome, email, idproduto, preco) VALUES ('{cnpj}', '{nome}', '{email}', {id_produto}, {preco})"
        else:
            statement = f"INSERT INTO fornecedor (cnpj, nome, idproduto, preco) VALUES ('{cnpj}', '{nome}', {id_produto}, {preco})"
        
        return self.db.execute_statement(statement)

    def atualiza_fornecedor(self, cnpj: str, nome: str = None, telefone: int = None, email: str = None, id_produto: int = None, preco: int = None):
        updates = []
        if nome:
            updates.append(f"nome = '{nome}'")
        if telefone is not None:
            updates.append(f"telefone = {telefone}")
        if email:
            updates.append(f"email = '{email}'")
        if id_produto is not None:
            updates.append(f"idproduto = {id_produto}")
        if preco is not None:
            updates.append(f"preco = {preco}")
        
        if not updates:
            return False
        
        statement = f"UPDATE fornecedor SET {', '.join(updates)} WHERE cnpj = '{cnpj}'"
        return self.db.execute_statement(statement)

    def deleta_fornecedor(self, cnpj: str):
        statement = f"DELETE FROM fornecedor WHERE cnpj = '{cnpj}'"
        return self.db.execute_statement(statement)


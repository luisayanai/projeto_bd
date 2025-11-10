# Conecta ao banco de dados e executa comandos SQL

from typing import Any
import psycopg2
from psycopg2.extras import DictCursor

class DatabaseManager:
    "Classe de Gerenciamento do database"

    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            dbname="tutorial",
            user="postgres", 
            password="654321",
            host="127.0.0.1", #localhost
            port=5432,
        )
        self.cursor = self.conn.cursor(cursor_factory=DictCursor) #maneira que o db vai retornar as coisas para nos (como um dict do python)
        
    def execute_statement(self, statement: str) -> bool:
        "Usado para Inserções, Deleções, Alter Tables"
        try:
            self.cursor.execute(statement)
            self.conn.commit()
        except:
            self.conn.reset()
            return False # se aconteceu erro na execução do comando sql no postgres
        return True

    # funcao para executar selects. Qualquer tipo de select e mandado para aqui e, entao, retorna lista (cada item e equivalente a um registro (linha retornada pelo SELECT))
    def execute_select_all(self, query: str) -> list[dict[str, Any]]:
        "Usado para SELECTS no geral"
        self.cursor.execute(query)
        return [dict(item) for item in self.cursor.fetchall()]

    # Para querries que executam uma vez so
    def execute_select_one(self, query: str) -> dict | None:
        "Usado para SELECT com apenas uma linha de resposta"
        self.cursor.execute(query)
        query_result = self.cursor.fetchone()

        if not query_result:
            return None

        return dict(query_result)
    
    
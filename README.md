# 🧵 Projeto BD - Curious about fashion

## 🔍 Visao geral
Dashboard web para consultar relatorios de vendas e estoque de uma loja, com API Flask + PostgreSQL e frontend estatico em HTML/CSS/JS.

## ✅ Requisitos
- Python 3.10+ e pip
- PostgreSQL acessivel em 127.0.0.1:5432 (ajuste em `backend/servicos/database/conector.py`)
- Navegador moderno para o frontend
- Sem uso de venv neste setup; instale as dependencias direto ou no ambiente Python que preferir

## 🗃️ Preparar banco de dados
1. Crie um database (padrao `bdddd`) e um usuario com acesso (padrao `postgres` com senha `654321`, configurado em `conector.py`).
2. Ajuste `backend/servicos/database/conector.py` se usar outro nome de database, host, usuario ou senha.
3. Aplique o script SQL de criacao/populacao (arquivos `script.txt` e `queries.txt` trazem consultas usadas e exemplos de dados).

## 🖥️ Executar backend (API Flask)
1. `cd backend`
2. `pip install -r requirements.txt`
3. `python main.py`
   - API sobe em `http://localhost:8000`
   - Blueprints expostos em `/rotas` e `/relatorios` atendem ao frontend

## 🧭 Executar frontend
- A URL base usada pelo JS esta em `frontend/app.js` (`http://localhost:8000`).
Escolha uma das opcoes:
1. Abrir `frontend/index.html` direto no navegador.
2. Ou servir localmente: `cd frontend` e `python -m http.server 5500`, depois abra `http://localhost:5500`.

## 🗂️ Estrutura do repositorio
- `backend/main.py` - inicializa Flask e registra rotas
- `backend/rotas/` - endpoints por dominio (cliente, produto, pedido, relatorios etc.)
- `backend/servicos/` - regras de negocio e consultas SQL
- `backend/servicos/database/conector.py` - conexao com PostgreSQL
- `backend/requirements.txt` - dependencias do backend
- `frontend/index.html`, `frontend/style.css`, `frontend/app.js` - SPA estatica que consome a API
- `script.txt`, `queries.txt` - scripts SQL de apoio

## 🛠️ Tecnologias
- Python, Flask, psycopg2
- PostgreSQL
- HTML, CSS, JavaScript puro

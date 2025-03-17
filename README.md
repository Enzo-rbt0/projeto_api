Projeto API FastAPI com SQLAlchemy

Este projeto é uma API desenvolvida em FastAPI que gerencia usuários, permitindo operações básicas de CRUD (Create, Read, Update, Delete). Ele utiliza o SQLAlchemy para interagir com um banco de dados MySQL, garantindo uma integração eficiente e segura com o banco de dados.


Funcionalidades Principais:

Inserir Usuário: Cria um novo usuário no banco de dados.

Listar Usuários: Retorna uma lista de todos os usuários cadastrados.

Buscar Usuário por ID: Retorna os detalhes de um usuário específico.

Atualizar Usuário: Atualiza os dados de um usuário existente.

Excluir Usuário: Remove um usuário do banco de dados.


Tecnologias Utilizadas:

FastAPI: Framework moderno e rápido para construção de APIs em Python.

SQLAlchemy: ORM (Object-Relational Mapping) para interação com o banco de dados.

MySQL: Banco de dados relacional para armazenamento de dados.

Pydantic: Validação de dados e serialização.

Uvicorn: Servidor ASGI para rodar a aplicação FastAPI.


Como Executar o Projeto:

Clone o repositório:

git clone https://github.com/Enzo-rbt0/projeto_api.git
Instale as dependências:

pip install -r requirements.txt
Configure o banco de dados no arquivo app/database/session.py.

Execute o servidor:

python run.py
Acesse a API em http://localhost:8080 e explore os endpoints usando o Swagger UI (/docs) ou o ReDoc (/redoc).

Endpoints da API:
POST /usuarios/inserir: Insere um novo usuário.

GET /usuarios/listar: Lista todos os usuários.

GET /usuarios/buscar/{user_id}: Busca um usuário por ID.

PUT /usuarios/atualizar/{user_id}: Atualiza um usuário existente.

DELETE /usuarios/excluir/{user_id}: Exclui um usuário.



Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

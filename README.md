# mvp-atividadefisica-backend
Projeto para a disciplina de desenvolvimento fullstack Puc-Rio
# Sobre o projeto

Este projeto consiste em uma API REST desenvolvida para realizar o gerenciamento de atividades físicas.
A API permite cadastrar, consultar, atualizar e excluir atividades físicas, armazenando os dados em um banco de dados SQLite.
O projeto foi desenvolvido como uma aplicação prática para estudo de desenvolvimento de software, integração entre back-end e banco de dados e criação de APIs REST.

# Tecnologias utilizadas
Python
Flask 3.0.3
SQLite
Flask-CORS
Flasgger / Swagger
REST API
As dependências utilizadas estão especificadas no arquivo requirements.txt.
Estrutura do Back-end
backend/
│
├── app.py
├── database.py
├── atividades.db
└── requirements.txt

app.py
Arquivo principal da aplicação.
É responsável por:
inicializar a aplicação Flask;
configurar o CORS;
configurar a documentação Swagger;
criar as rotas da API;
validar os dados recebidos;
realizar operações de CRUD;
retornar os dados em formato JSON.

database.py
Responsável pela configuração e comunicação com o banco de dados SQLite.
Também define os tipos de atividade e os níveis de intensidade aceitos pela aplicação.

atividades.db
Banco de dados SQLite utilizado para armazenar as atividades cadastradas.

requirements.txt
Arquivo que contém as dependências necessárias para executar o projeto.

# Banco de dados
O sistema utiliza SQLite.
A tabela principal é:

CampoTipoDescrição

id
INTEGER
Identificador único


tipo
TEXT
Tipo da atividade


data
DATE
Data da atividade


duracao
INTEGER
Duração em minutos


distancia
REAL
Distância percorrida


intensidade
TEXT
Intensidade do exercício


observacoes
TEXT
Observações adicionais

Os tipos de atividade disponíveis são:
Corrida
Caminhada
Ciclismo
Musculação
Natação
Surf
Outro
Os níveis de intensidade disponíveis são:
Baixa
Média
Alta
 # Endpoints
 Criar atividade
POST /atividades

Exemplo de requisição:
{
    "tipo": "Corrida",
    "data": "2026-09-13",
    "duracao": 45,
    "distancia": 6.2,
    "intensidade": "Alta",
    "observacoes": "Treino pela manhã"
}

Retorna os dados da atividade cadastrada.

 ## Listar atividades
GET /atividades

Retorna todas as atividades cadastradas.
As atividades são organizadas por data, da mais recente para a mais antiga.

 ## Buscar uma atividade
GET /atividades/<id>

Exemplo:
GET /atividades/1

## Retorna uma atividade específica.
Caso o ID não exista, a API retorna erro 404.

 ## Atualizar atividade
PUT /atividades/<id>

Permite alterar os dados de uma atividade existente.

## Excluir atividade
DELETE /atividades/<id>

Remove uma atividade do banco de dados.
Em caso de sucesso, a API retorna o status 204.

## Validação dos dados
A API realiza validações antes de inserir ou atualizar uma atividade.
Entre elas:
verificação dos campos obrigatórios;
validação do tipo de atividade;
validação da intensidade;
verificação de duração positiva;
verificação de distância não negativa;
validação dos tipos numéricos.
Os campos obrigatórios para o cadastro são:
tipo
data
duracao
intensidade

# Documentação da API
A aplicação utiliza Flasgger para disponibilizar documentação baseada em Swagger.
A documentação descreve a API e seus endpoints diretamente no projeto.
 Como executar
1. Clonar o projeto
git clone <URL_DO_REPOSITORIO>
cd <PASTA_DO_PROJETO>

2. Criar um ambiente virtual
python -m venv venv

3. Ativar o ambiente virtual
No Windows:
venv\Scripts\activate

No Linux/macOS:
source venv/bin/activate

4. Instalar as dependências
pip install -r requirements.txt

5. Executar a aplicação
python app.py

A aplicação será executada na porta 5000.
http://localhost:5000

O banco de dados é inicializado pela aplicação quando ela é executada.
🔄 Funcionamento
O fluxo básico da aplicação é:
Front-end
    ↓
Requisição HTTP
    ↓
API Flask
    ↓
Validação dos dados
    ↓
SQLite
    ↓
Resposta JSON
    ↓
Front-end


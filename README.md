# Projeto APIs para Agentes de IA
Esse é um Projeto de exemplo de uma API para suportar operações de agente baseados em LLMs. Foi criada uma API RESTful com [Flask](https://flask.palletsprojects.com/en/stable/), [SQLAlchemy](https://www.sqlalchemy.org/), [Gunicorn](https://gunicorn.org/) e Docker e contruida com uma arquitetura MSCR. Já os agentes foi construídos usando principalmente a biblioteca [LangGraph](https://docs.langchain.com/).

O projeto tem como objetivo ser um ambiente para experimentos com agentes de IA, registrando versões de modelos, prompts, conversas e métricas, além de ter um padrão arquitetural pronto para produção, servindo de inspiração para aplicações profissionais futuras.

A versão atual do projeto já tem implementado uma API simples que salva chats e conversas em um banco de dados SQLite e um agente simples com apenas um nó de LLM e um nó de tools e uma memória gerenciada com Redis.

# Estrutura
<pre>
app/
├── wsgi.py                         # execução da aplicação com create_app
│
├── api/                            # módulo da API
│   ├── models/                     # entidades do banco
│   ├── repositories/               # acesso ao banco
│   ├── services/                   # regras de negócio
│   ├── controllers/                # recursos da api
│   └── config/                     # configurações
│       ├── db_config.py            # configuração do banco (SQL Alchemy)
│       ├── flask_config.py         # configuração da aplicação Flask
│       └── restx_config.py         # configuração da API RESTful
│
├── agent/                          # módulo do agente
│   ├── facade/                     # ponto único de entrada do agente
│   │   └── policies/               # políticas (por enquanto possui somente guardrails de entrada e saída)
│   ├── factory/                    # cria o agente
│   ├── runners/                    # executor concreto do agente
│   ├── prompts/                    # versionamento dos prompts
│   ├── tools/                      # ferramentas do agente
│   └── memory/                     # in memory com redis
│
├── infrastructure/                 # implementação tecnica concreta
│   ├── clients/                    # adapters de serviços externos usados (por enquanto somente o do MLflow foi implementado)
│   ├── knowledge/                  # armazena as bases de conhecimento dos agentes e as ferramentas para sua consulta
│   └── observability/              # cria as estruturas de métricas
│
├── tests/                          # módulo de testes (ainda vazio)
│   ├── unit/                       # domínio e políticas
│   ├── integration/                # agente
│   └── e2e/                        # API completa
│
├── instances/                      # banco de dados
│
├── create_app.py                   # reúne todos os componentes da API e implementa a função de criar a api
│
├── docker-compose.yml              # configuração dos containers
│
├── Dockerfile                      # instruções de execução para construção da API dentro do container
│
└── requirements.txt                # dependências
</pre>

# Instruções para a execução
1. Navegue para o diretório do projeto ``./exemplo_api_ai``.
2. Configure o arquivo .env com a chave da API do Groq (GROQ_API_KEY) e o URI do banco de dados (DATABASE_URI)
3. execute o docker compose:
   ```sh
   docker-compose up --build
   ```
4. Acompanhe as mensagens no terminal e espere a aplicação inicializar.
5. Para acessar a api, navegue para `http:/localhost:5000`.
6. Nos recursos de Chat, crie um chat e depois consulte seu UUID.
7. Nos recursos de Chatbot, teste o agente escrevendo uma entrada e preenchendo o UUID da sua conversa.
8. Se estiver usando um banco SQLite, baixe a extensão SQLite Viewer e clique com botão esquerdo no arquivo .db em `./instances` para visualizar.

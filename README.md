### Monitoramento1 

Montando e Executando
docker build -t monitoramento-web .

Run
docker run --rm monitoramento-web
Ira exibir os dados na tela

### Monitoramento2 

1. Visão Geral do Projeto
O objetivo é monitorar disponibilidade (ping) e performance (tempo de carregamento HTTP) de sites selecionados, com visualização dos resultados via dashboard em Grafana. Todos os componentes rodam isolados em containers Docker, facilitando deploy, portabilidade e integração com banco de dados e ferramentas externas.

2. Arquitetura de Alto Nível
Visão em Blocos

┌────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
│ Script Agente  │ --> │ Banco de Dados      │ --> │ Grafana         │
│ Monitoramento  │     │ PostgreSQL container│     │ Dashboard       │
└────────────────┘     └─────────────────────┘     └─────────────────┘
          ↑
          │
      [Docker Compose]

Descrição dos blocos:

Agente Monitoramento (webmonitor_agent): Script Python em container Docker que executa pings e requisições HTTP, grava resultados no banco.
Banco de Dados PostgreSQL: Armazena resultados dos testes para análise e visualização.
Grafana: Exibe dashboards em tempo real, consumindo dados do PostgreSQL.

3. Tecnologias Principais
Python (ping3, requests, time): Para lógica de coleta e testes.
Docker & Docker Compose: Para empacotamento, rede e gerenciamento dos ambientes.
PostgreSQL: Persistência dos resultados dos testes.
Grafana: Visualização web dos resultados.
Linux (Bash): Execução dos containers e automação.

4. Fluxo Funcional
Execução dos Testes

O agente percorre uma lista de sites (google.com, youtube.com, rnt.br).
Para cada site, realiza:
Ping: Calcula latência média e perda de pacotes.
HTTP GET: Mede tempo de carregamento e código de status HTTP.
Persistência

Os resultados são gravados em uma tabela chamada resultados no PostgreSQL.
Cada registro inclui: site, timestamp, tipo de teste, valor do teste (latência, perda, código, tempo, etc).
Visualização e Dashboards

O Grafana coleta dados do banco e exibe gráficos de latência, perda de pacote, tempo de resposta e disponibilidade dos sites.

5. Componentes Principais

COMPONENTE	DESCRIÇÃO
Agente Monitoramento	Script Python, roda em container, executa testes.
PostgreSQL	Banco no container para persistir resultados.
Grafana	Dashboard web para visualização dos dados.
Docker Compose	Orquestra todos os containers e redes.

6. Fluxo de Deploy & Operação

1. Rodando com Docker Compose:
docker-compose up --build

2. Monitoramento:
O agente executa periodicamente ou via cron (melhoria futura).

3. Consulta ao Banco:
Comando para acessar o banco via terminal:

docker exec -it src-postgres_webmonitor-1 bash
psql -h localhost -U monitoruser -d monitor

4. Acessando o Grafana:
URL: 
localhost:3000
Usuário: admin, senha: admin (padrão)

7. Diagrama Simplificado

[ Monitoramento Agent ]
        |
        v
[ PostgreSQL - resultados ]
        |
        v
[ Grafana Dashboard ]

8. Exemplo de Consulta SQL Grafana

SELECT
  time_column AS "time",
  valor
FROM
  resultados
ORDER BY time_column

## Monitoramento 3

Monitoramento da API ViaIPE

1. Objetivo do Projeto
Coletar estatísticas de disponibilidade de clientes publicados pela API oficial do viaipe.rnp.br, processar, calcular indicadores e visualizar essas informações em dashboards para monitoramento, usando uma stack moderna e portátil baseada em Docker e Docker Compose.

2. Arquitetura Geral
Visão de Alto Nível

          +---------------+
          |   ViaIPE API  |
          +-------+-------+
                  |
          [1-HTTP Fetch]
                  |
          +-------v--------+         +----------------+
          | Python/Flask   |         |   Grafana      |
          | App/API        +---------> (Dashboard)    |
          +-------+--------+   [2]   +-------^--------+
                  |                    |
          [3-ORM + SQLAlchemy]         |
                  |                    |
            +-----v------+             |
            | PostgreSQL |<------------+
            +------------+

Componentes Principais
ViaIPE API: Fornece JSON com clientes de um determinado ponto de presença na RNP (Ex: /api/norte).
Python Flask App: Consulta periodicamente a API do ViaIPE, processa os dados, calcula estatísticas e armazena no PostgreSQL. Disponibiliza endpoints REST para importação e consulta.
PostgreSQL: Banco relacional para persistência dos registros.
Grafana: Visualiza os dados armazenados em tempo real e constrói dashboards interativos.
Docker Compose: Orquestra todos os serviços de forma isolada e reprodutível.

3. Fluxos de Dados & Processos

3.1. Coleta de Dados
Um serviço Python/Flask expõe um endpoint (/importa_api) que, quando chamado, faz requisição HTTP GET para a API do ViaIPE.
Exemplo:
GET https://viaipe.rnp.br/api/norte
Os dados recebidos (campos como uf, cidade, nome, ip) são processados para cada cliente e armazenados em uma tabela no PostgreSQL.

3.2. Cálculo de Disponibilidade
O app pode (a cada importação ou com agendador futuro) calcular médias como:
Disponibilidade média dos clientes
Total por Estado ou Cidade
Histórico de variações
Os cálculos são implementados via queries SQL ou processamento Python (pode ser incrementado conforme análise futura).

3.3. Visualização em Dashboard
O Grafana acessa o PostgreSQL via conexão configurada (db:5432) e consome as tabelas pré-preenchidas.
Dashboards são montados via queries SQL customizadas, exibindo indicadores como:
Número total de clientes por UF/cidade
Disponibilidade e variações (quando disponível nos dados)
Evolução temporal (caso haja histórico)
Grafana se conecta no PostgreSQL de forma nativa, permitindo análises e visualizações automáticas. http://localhost:3000/login 

4. Tecnologias Utilizadas

COMPONENT	STACK/VERSION	FUNÇÃO
Backend Service	Python 3 + Flask	Orquestra coleta & API
ORM	SQLAlchemy	Modelagem/queries no PostgreSQL
Banco de Dados	PostgreSQL 16	Persistência de registros
Visualização	Grafana	Dashboards e visual analytics
Orquestração	Docker + Compose	Containerização do projeto


# Projeto de Portfólio: Pipeline de ETL e Dashboard de Vendas

## 🎯 Objetivo
Este projeto implementa um pipeline de ETL completo para processar dados de vendas do dataset público da Olist. Os dados brutos são extraídos de arquivos CSV, transformados com Python (Pandas), carregados em um banco de dados PostgreSQL e, por fim, visualizados em um dashboard interativo.

## 🚀 Tecnologias Utilizadas
- **Linguagem:** Python
- **Bibliotecas:** Pandas, SQLAlchemy
- **Banco de Dados:** PostgreSQL
- **Ferramenta de BI:** Google Looker Studio
- **Ambiente:** Jupyter Notebook (para exploração) e script .py (para automação)

## 📁 Estrutura do Projeto
- `etl.py`: Script principal que executa todo o pipeline de ETL de forma automatizada.
- `exploracao_etl.ipynb`: Jupyter Notebook contendo a análise exploratória, o desenvolvimento da lógica de ETL e as queries SQL para a criação do dashboard.
- `dados/`: Contém os datasets brutos em formato CSV.
- `dashboard_data/`: Contém os dados agregados usados como fonte para o dashboard.
- `schema.sql`: Contém o código SQL para a criação das tabelas no PostgreSQL.

## 📊 Dashboard
O dashboard interativo apresenta os principais indicadores de negócio, como receita mensal, top categorias de produtos e distribuição de clientes por estado.

**[>> Clique aqui para ver o dashboard interativo <<](https://lookerstudio.google.com/reporting/74848e0d-43a6-4637-bb43-b380ca1b9603)**

## ⚙️ Como Executar

Para replicar este projeto em seu ambiente local, siga os passos abaixo.

### 1. Pré-requisitos
- Ter o [Python 3](https://www.python.org/downloads/) instalado.
- Ter o [PostgreSQL](https://www.postgresql.org/download/) instalado. O **pgAdmin**, que é a interface gráfica, geralmente é incluído na instalação.

### 2. Configuração do Banco de Dados
1.  **Crie o Banco de Dados:** Usando o **pgAdmin**, crie um novo banco de dados com o nome `olist_db`.
2.  **Crie as Tabelas:** Abra a "Query Tool" (Ferramenta de Consulta) para o banco `olist_db`. Copie todo o conteúdo do arquivo `schema.sql` deste repositório, cole na Query Tool e execute o script. Isso criará todas as tabelas e relacionamentos necessários.

### 3. Configuração do Projeto
1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/AndreVVoigt/projeto-etl-olist
    ```
2.  **Instale as Dependências:**
    ```bash
    pip install pandas sqlalchemy psycopg2-binary
    ```
3.  **Adicione os Dados Brutos:** Baixe o dataset da Olist do Kaggle [https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?resource=download](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?resource=download) e coloque todos os arquivos `.csv` dentro da pasta `dados/`.
4.  **Configure a Conexão:** No arquivo `etl.py`, atualize a variável `db_password` com a sua senha do PostgreSQL.

### 4. Execução do Pipeline
1.  Execute o script de ETL através do terminal:
    ```bash
    python etl.py
    ```
2.  O script irá limpar as tabelas (se já tiverem dados) e carregar os dados processados do CSV para o PostgreSQL.
3.  Após a execução, você pode usar o **pgAdmin** para se conectar ao banco `olist_db` e verificar se os dados foram carregados corretamente nas tabelas.

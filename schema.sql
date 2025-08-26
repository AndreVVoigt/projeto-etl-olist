-- Este script cria a estrutura de tabelas (schema) para o projeto de ETL da Olist.
-- As tabelas são divididas em dimensões (dim) e fatos (fato).

-- Tabela de Dimensão para armazenar informações de clientes
CREATE TABLE dim_clientes (
    cliente_id VARCHAR(255) PRIMARY KEY,
    cliente_zip_code_prefix INT,
    cliente_cidade VARCHAR(255),
    cliente_estado VARCHAR(2)
);

-- Tabela de Dimensão para armazenar informações de produtos
CREATE TABLE dim_produtos (
    produto_id VARCHAR(255) PRIMARY KEY,
    produto_categoria VARCHAR(255),
    produto_fotos_qtd INT
);

-- Tabela de Fatos para armazenar os eventos de pedido
-- Esta tabela possui chaves estrangeiras que se conectam às tabelas de dimensão.
CREATE TABLE fato_pedidos (
    pedido_id VARCHAR(255),
    item_pedido_id INT,
    produto_id VARCHAR(255) REFERENCES dim_produtos(produto_id),
    vendedor_id VARCHAR(255),
    cliente_id VARCHAR(255) REFERENCES dim_clientes(cliente_id),
    status_pedido VARCHAR(255),
    preco NUMERIC(10, 2),
    frete NUMERIC(10, 2),
    data_pedido TIMESTAMP,
    data_aprovado TIMESTAMP,
    data_enviado TIMESTAMP,
    data_entregue TIMESTAMP,
    data_entrega_estimada TIMESTAMP,
    PRIMARY KEY (pedido_id, item_pedido_id)
);

-- Tabela de Fatos para informações de pagamento
CREATE TABLE fato_pagamentos (
    pedido_id VARCHAR(255),
    pagamento_sequencial INT,
    tipo_pagamento VARCHAR(255),
    pagamento_prestacoes INT,
    valor_pagamento NUMERIC(10, 2),
    PRIMARY KEY (pedido_id, pagamento_sequencial)
);
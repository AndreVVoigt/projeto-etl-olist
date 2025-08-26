import pandas as pd
from sqlalchemy import create_engine, text
import os

def etl_pipeline():
    """
    Função principal que executa o pipeline de ETL completo.
    """
    db_user = 'postgres'
    db_password = '1234'
    db_host = 'localhost'
    db_port = '5432'
    db_name = 'olist_db'
    
    try:
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        print("Conexão com o banco de dados estabelecida com sucesso.")
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return

    # --- 1. EXTRAÇÃO ---
    print("\nIniciando a fase de Extração...")
    caminho_dados = 'dados'
    dataframes = {}
    arquivos_csv = [
        'olist_customers_dataset.csv', 'olist_products_dataset.csv', 'olist_orders_dataset.csv',
        'olist_order_items_dataset.csv', 'olist_order_payments_dataset.csv'
    ]
    
    for arquivo in arquivos_csv:
        nome_df = arquivo.split('_dataset.csv')[0].replace('olist_', '')
        caminho_completo = os.path.join(caminho_dados, arquivo)
        dataframes[nome_df] = pd.read_csv(caminho_completo)
    print("Dados extraídos dos arquivos CSV.")

    # --- 2. TRANSFORMAÇÃO ---
    print("\nIniciando a fase de Transformação...")
    
    # Transformação de Clientes
    dim_clientes = dataframes['customers'].rename(columns={
        'customer_id': 'cliente_id', 'customer_zip_code_prefix': 'cliente_zip_code_prefix',
        'customer_city': 'cliente_cidade', 'customer_state': 'cliente_estado'
    })[['cliente_id', 'cliente_zip_code_prefix', 'cliente_cidade', 'cliente_estado']]

    # Transformação de Produtos
    dim_produtos = dataframes['products'].rename(columns={
        'product_id': 'produto_id', 'product_category_name': 'produto_categoria',
        'product_photos_qty': 'produto_fotos_qtd'
    })
    dim_produtos['produto_categoria'] = dim_produtos['produto_categoria'].fillna('outros')
    dim_produtos = dim_produtos[['produto_id', 'produto_categoria', 'produto_fotos_qtd']]

    # Transformação de Pagamentos
    fato_pagamentos = dataframes['order_payments'].rename(columns={
        'order_id': 'pedido_id', 'payment_sequential': 'pagamento_sequencial',
        'payment_type': 'tipo_pagamento', 'payment_installments': 'pagamento_prestacoes',
        'payment_value': 'valor_pagamento'
    })

    # Transformação de Pedidos
    fato_pedidos = pd.merge(dataframes['orders'], dataframes['order_items'], on='order_id', how='inner')
    fato_pedidos = fato_pedidos.rename(columns={
        'order_id': 'pedido_id', 'order_item_id': 'item_pedido_id', 'product_id': 'produto_id',
        'seller_id': 'vendedor_id', 'customer_id': 'cliente_id', 'order_status': 'status_pedido',
        'price': 'preco', 'freight_value': 'frete', 'order_purchase_timestamp': 'data_pedido',
        'order_approved_at': 'data_aprovado', 'order_delivered_carrier_date': 'data_enviado',
        'order_delivered_customer_date': 'data_entregue', 'order_estimated_delivery_date': 'data_entrega_estimada'
    })
    colunas_data = ['data_pedido', 'data_aprovado', 'data_enviado', 'data_entregue', 'data_entrega_estimada']
    for col in colunas_data:
        fato_pedidos[col] = pd.to_datetime(fato_pedidos[col], errors='coerce')
    fato_pedidos = fato_pedidos[['pedido_id', 'item_pedido_id', 'produto_id', 'vendedor_id', 'cliente_id', 'status_pedido', 'preco', 'frete', 'data_pedido', 'data_aprovado', 'data_enviado', 'data_entregue', 'data_entrega_estimada']]
    
    print("Dados transformados com sucesso.")

    # --- 3. CARREGAMENTO ---
    print("\nIniciando a fase de Carregamento...")
    try:
        # Limpando as tabelas antes de inserir novos dados
        with engine.connect() as connection:
            print("Limpando dados das tabelas existentes...")
            tabelas_para_limpar = ['fato_pagamentos', 'fato_pedidos', 'dim_clientes', 'dim_produtos']
            for tabela in tabelas_para_limpar:
                connection.execute(text(f'DELETE FROM {tabela};'))
            connection.commit()
            print("Tabelas limpas.")

        # Carregando os dataframes para o banco de dados
        dim_clientes.to_sql('dim_clientes', engine, if_exists='append', index=False)
        dim_produtos.to_sql('dim_produtos', engine, if_exists='append', index=False)
        fato_pedidos.to_sql('fato_pedidos', engine, if_exists='append', index=False)
        fato_pagamentos.to_sql('fato_pagamentos', engine, if_exists='append', index=False)
        
        print("\nCarga de dados concluída com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro durante a fase de Carga: {e}")

if __name__ == '__main__':
    etl_pipeline()
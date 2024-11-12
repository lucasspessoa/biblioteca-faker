import pandas as pd
import numpy as np
from faker import Faker

# Instanciar o gerador de dados Faker
fake = Faker()

# Fixar uma semente para reprodutibilidade
np.random.seed(0)

# Configurações para simular dados
num_clients = 10000
num_products = 500
num_transactions = 100000
num_feedbacks = 50000

# 1. Clientes
clients_data = {
    "ID_Cliente": range(1, num_clients + 1),
    "Nome_Cliente": [fake.name() for _ in range(num_clients)],
    "Idade": np.random.randint(18, 80, num_clients),
    "Sexo": np.random.choice(["M", "F"], num_clients),
    "Cidade": [fake.city() for _ in range(num_clients)],
    "Estado": [fake.state_abbr() for _ in range(num_clients)],
    "Data_Registro": [fake.date_this_decade() for _ in range(num_clients)],
    "Renda_Anual": np.random.randint(20000, 150000, num_clients),
    "Categoria_Cliente": np.random.choice(["Novo", "Recorrente", "VIP"], num_clients, p=[0.5, 0.4, 0.1])
}
clients_df = pd.DataFrame(clients_data)

# 2. Produtos
products_data = {
    "ID_Produto": range(1, num_products + 1),
    "Nome_Produto": [fake.word() for _ in range(num_products)],
    "Categoria": np.random.choice(["Eletrônicos", "Vestuário", "Alimentos", "Casa", "Esportes"], num_products),
    "Preço_Unitário": np.round(np.random.uniform(10, 1000, num_products), 2),
    "Data_Lancamento": [fake.date_this_decade() for _ in range(num_products)],
    "Fornecedor": [fake.company() for _ in range(num_products)]
}
products_df = pd.DataFrame(products_data)

# 3. Transações
transactions_data = {
    "ID_Transacao": range(1, num_transactions + 1),
    "Data_Compra": [fake.date_this_year() for _ in range(num_transactions)],
    "ID_Cliente": np.random.choice(clients_df["ID_Cliente"], num_transactions),
    "ID_Produto": np.random.choice(products_df["ID_Produto"], num_transactions),
    "Quantidade_Vendida": np.random.randint(1, 10, num_transactions),
    "Metodo_Pagamento": np.random.choice(["Cartão de Crédito", "Pix", "Boleto"], num_transactions)
}
transactions_df = pd.DataFrame(transactions_data)

# Cálculo do Valor Total da Venda (Preço Unitário * Quantidade)
transactions_df = transactions_df.merge(products_df[['ID_Produto', 'Preço_Unitário']], on="ID_Produto")
transactions_df["Valor_Total_Venda"] = transactions_df["Quantidade_Vendida"] * transactions_df["Preço_Unitário"]
transactions_df.drop(columns="Preço_Unitário", inplace=True)

# 4. Feedbacks
feedback_data = {
    "ID_Feedback": range(1, num_feedbacks + 1),
    "ID_Transacao": np.random.choice(transactions_df["ID_Transacao"], num_feedbacks),
    "ID_Cliente": np.random.choice(clients_df["ID_Cliente"], num_feedbacks),
    "Nota": np.random.randint(1, 6, num_feedbacks),
    "Comentario": [fake.sentence() for _ in range(num_feedbacks)]
}
feedback_df = pd.DataFrame(feedback_data)

# Exportar as tabelas para um arquivo Excel com várias abas
file_path = "desafio_segmentacao_clusterizacao.xlsx"
with pd.ExcelWriter(file_path) as writer:
    clients_df.to_excel(writer, sheet_name="Clientes", index=False)
    products_df.to_excel(writer, sheet_name="Produtos", index=False)
    transactions_df.to_excel(writer, sheet_name="Transacoes", index=False)
    feedback_df.to_excel(writer, sheet_name="Feedback", index=False)

file_path

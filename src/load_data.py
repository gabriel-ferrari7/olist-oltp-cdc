import sqlite3
import pandas as pd

DB_PATH = "db/olist.sqlite"
CUSTOMERS_CSV = "data/raw/olist_customers_dataset.csv"
ORDERS_CSV = "data/raw/olist_orders_dataset.csv"
ORDER_ITEMS_CSV = "data/raw/olist_order_items_dataset.csv"
ORDER_PAYMENTS_CSV = "data/raw/olist_order_payments_dataset.csv"


def limpar_tabelas(cursor):
    cursor.execute("DELETE FROM order_payments")
    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM customers")


def carregar_customers(cursor):
    df_customers = pd.read_csv(
        CUSTOMERS_CSV,
        dtype={"customer_zip_code_prefix": str}
    )

    for linha in df_customers.itertuples():
        cursor.execute(
    """
    INSERT INTO customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        linha.customer_id,
        linha.customer_unique_id,
        linha.customer_zip_code_prefix,
        linha.customer_city,
        linha.customer_state,
    )
)

    print(f"{len(df_customers)} clientes inseridos.")


def carregar_orders(cursor):
    df_orders = pd.read_csv(ORDERS_CSV)
    df_orders = df_orders.where(pd.notnull(df_orders), None)

    for linha in df_orders.itertuples():
        cursor.execute(
    """
    INSERT INTO orders (order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        linha.order_id,
        linha.customer_id,
        linha.order_status,
        linha.order_purchase_timestamp,
        linha.order_approved_at,
        linha.order_delivered_carrier_date,
        linha.order_delivered_customer_date,
        linha.order_estimated_delivery_date,
    )
)

    print(f"{len(df_orders)} pedidos inseridos.")

def carregar_order_items(cursor):
    df_order_items = pd.read_csv(ORDER_ITEMS_CSV)
    df_order_items = df_order_items.where(pd.notnull(df_order_items), None)

    for linha in df_order_items.itertuples():
        cursor.execute(
    """
    INSERT INTO order_items (order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        linha.order_id,
        linha.order_item_id,
        linha.product_id,
        linha.seller_id,
        linha.shipping_limit_date,
        linha.price,
        linha.freight_value,
    )
)

    print(f"{len(df_order_items)} itens de pedido inseridos.")


def carregar_order_payments(cursor):
    df_order_payments = pd.read_csv(ORDER_PAYMENTS_CSV)
    df_order_payments = df_order_payments.where(pd.notnull(df_order_payments), None)

    for linha in df_order_payments.itertuples():
        cursor.execute(
    """
    INSERT INTO order_payments (order_id, payment_sequential, payment_type, payment_installments, payment_value)
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        linha.order_id,
        linha.payment_sequential,
        linha.payment_type,
        linha.payment_installments,
        linha.payment_value,
    )
)

    print(f"{len(df_order_payments)} pagamentos inseridos.")

def main():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    try:
        limpar_tabelas(cursor)
        carregar_customers(cursor)
        carregar_orders(cursor)
        carregar_order_items(cursor)
        carregar_order_payments(cursor)
        conexao.commit()
    finally:
        conexao.close()


if __name__ == "__main__":
    main()
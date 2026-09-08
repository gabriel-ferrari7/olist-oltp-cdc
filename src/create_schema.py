import sqlite3

DB_PATH = "db/olist.sqlite"


def criar_schema():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    try:
        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                customer_unique_id TEXT,
                customer_zip_code_prefix TEXT,
                customer_city TEXT,
                customer_state TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                customer_id TEXT,
                order_status TEXT,
                order_purchase_timestamp TEXT,
                order_approved_at TEXT,
                order_delivered_carrier_date TEXT,
                order_delivered_customer_date TEXT,
                order_estimated_delivery_date TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_id TEXT,
                order_item_id INTEGER,
                product_id TEXT,
                seller_id TEXT,
                shipping_limit_date TEXT,
                price REAL,
                freight_value REAL,
                PRIMARY KEY (order_id, order_item_id),
                FOREIGN KEY (order_id) REFERENCES orders (order_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_payments (
                order_id TEXT,
                payment_sequential INTEGER,
                payment_type TEXT,
                payment_installments INTEGER,
                payment_value REAL,
                PRIMARY KEY (order_id, payment_sequential),
                FOREIGN KEY (order_id) REFERENCES orders (order_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cdc_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                tabela TEXT,
                operacao TEXT,
                identificador TEXT,
                dados_antes TEXT,
                dados_depois TEXT
            )
        """)
        
        conexao.commit()
        print("Tabelas 'customers', 'orders', 'order_items', 'order_payments', 'cdc_log' criadas com sucesso!")

    finally:
        conexao.close()


if __name__ == "__main__":
    criar_schema()
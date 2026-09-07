import sqlite3
from cdc_logger import registrar_log

DB_PATH = "db/olist.sqlite"


def simular_entrega_pedido(cursor):
    cursor.execute("""
        SELECT order_id FROM orders
        WHERE order_status = 'shipped'
        ORDER BY RANDOM()
        LIMIT 1
    """)
    resultado = cursor.fetchone()

    if resultado is None:
        print("Nenhum pedido com status 'shipped' encontrado.")
        return

    order_id = resultado[0]
    status_antigo = "shipped"
    status_novo = "delivered"

    cursor.execute("""
        UPDATE orders
        SET order_status = ?
        WHERE order_id = ?
    """, (status_novo, order_id))

    registrar_log(
        cursor,
        tabela="orders",
        operacao="UPDATE",
        identificador=order_id,
        dados_antes={"order_status": status_antigo},
        dados_depois={"order_status": status_novo},
    )

    print(f"Pedido {order_id} atualizado de 'shipped' para 'delivered'.")

def simular_cancelamento_item(cursor):
    cursor.execute("""
        SELECT order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value
        FROM order_items
        ORDER BY RANDOM()
        LIMIT 1
    """)
    resultado = cursor.fetchone()

    if resultado is None:
        print("Nenhum item de pedido encontrado para cancelar.")
        return

    order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value = resultado

    cursor.execute("""
        DELETE FROM order_items
        WHERE order_id = ? AND order_item_id = ?
    """, (order_id, order_item_id))

    registrar_log(
        cursor,
        tabela="order_items",
        operacao="DELETE",
        identificador=f"{order_id}:{order_item_id}",
        dados_antes={
            "product_id": product_id,
            "seller_id": seller_id,
            "shipping_limit_date": shipping_limit_date,
            "price": price,
            "freight_value": freight_value,
        },
        dados_depois=None,
    )

    print(f"Item {order_item_id} do pedido {order_id} foi cancelado (removido).")


def simular_novo_pagamento(cursor):
    cursor.execute("""
        SELECT order_id FROM orders
        ORDER BY RANDOM()
        LIMIT 1
    """)
    resultado = cursor.fetchone()

    if resultado is None:
        print("Nenhum pedido encontrado para adicionar pagamento.")
        return

    order_id = resultado[0]

    cursor.execute("""
        SELECT MAX(payment_sequential) FROM order_payments
        WHERE order_id = ?
    """, (order_id,))
    maior_sequencial = cursor.fetchone()[0]

    novo_sequencial = maior_sequencial + 1
    payment_type = "voucher"
    payment_installments = 1
    payment_value = 50.0

    cursor.execute("""
        INSERT INTO order_payments VALUES (?, ?, ?, ?, ?)
    """, (order_id, novo_sequencial, payment_type, payment_installments, payment_value))

    registrar_log(
        cursor,
        tabela="order_payments",
        operacao="INSERT",
        identificador=f"{order_id}:{novo_sequencial}",
        dados_antes=None,
        dados_depois={
            "payment_type": payment_type,
            "payment_installments": payment_installments,
            "payment_value": payment_value,
        },
    )

    print(f"Novo pagamento (sequencial {novo_sequencial}) inserido para o pedido {order_id}.")


def main():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    try:
        simular_entrega_pedido(cursor)
        simular_cancelamento_item(cursor)
        simular_novo_pagamento(cursor)
        conexao.commit()
    finally:
        conexao.close()


if __name__ == "__main__":
    main()
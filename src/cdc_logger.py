import json
from datetime import datetime

LOG_FILE_PATH = "logs/cdc.log"


def registrar_log(cursor, tabela, operacao, identificador, dados_antes=None, dados_depois=None):
    timestamp = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO cdc_log (timestamp, tabela, operacao, identificador, dados_antes, dados_depois)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        tabela,
        operacao,
        identificador,
        json.dumps(dados_antes) if dados_antes else None,
        json.dumps(dados_depois) if dados_depois else None,
    ))

    _escrever_log_arquivo(timestamp, tabela, operacao, identificador, dados_antes, dados_depois)


def _escrever_log_arquivo(timestamp, tabela, operacao, identificador, dados_antes, dados_depois):
    linha = f"{timestamp} | {operacao} | {tabela} | {identificador} | antes={dados_antes} | depois={dados_depois}\n"

    with open(LOG_FILE_PATH, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)
import os
import time
import requests
from ping3 import ping
import psycopg2

# Config do banco pelo ambiente
DB_HOST = os.getenv('DB_HOST', 'monitoramento-db')
DB_NAME = os.getenv('DB_NAME', 'monitoramento')
DB_USER = os.getenv('DB_USER', 'monuser')
DB_PASS = os.getenv('DB_PASS', 'monsenha')

URLS = ["https://google.com", "https://youtube.com", "https://rnt.br"]

def wait_for_db():
    for i in range(15):
        try:
            conn = psycopg2.connect(
                host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
            )
            conn.close()
            print("Conectado ao banco!")
            return
        except Exception as e:
            print(f"Tentando conectar ao banco, tentativa {i+1}/15... (Erro: {e})")
            time.sleep(2)
    print("Não foi possível conectar no banco após várias tentativas.")
    exit(1)

def criar_tabela(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS resultados (
        id SERIAL PRIMARY KEY,
        tipo VARCHAR(10),
        destino VARCHAR(50),
        rtt FLOAT,
        perda_pct FLOAT,
        status_code VARCHAR(10),
        tempo FLOAT,
        dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

def inserir_resultado(cur, tipo, destino, rtt, perda_pct, status_code, tempo):
    cur.execute("""
        INSERT INTO resultados(tipo, destino, rtt, perda_pct, status_code, tempo)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (tipo, destino, rtt, perda_pct, status_code, tempo))

def testar_ping(host, count=4):
    latencias = []
    perdidos = 0
    for _ in range(count):
        rtt = ping(host, unit='ms')
        if rtt is not None:
            latencias.append(rtt)
        else:
            perdidos += 1
        time.sleep(1)
    perda_pct = (perdidos / count) * 100
    media_rtt = sum(latencias) / len(latencias) if latencias else None
    return media_rtt, perda_pct

def testar_http(url):
    try:
        inicio = time.time()
        resp = requests.get(url, timeout=10)
        duracao = time.time() - inicio
        return resp.status_code, duracao
    except requests.exceptions.RequestException as e:
        return str(e), None

def run_tests():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()
    criar_tabela(cur)
    print("== Teste de Ping ==")
    for url in URLS:
        host = url.replace("https://", "").replace("http://", "").split("/")[0]
        rtt, perda = testar_ping(host)
        print(f"{host}: RTT médio = {rtt}, Perda = {perda}")
        inserir_resultado(cur, "ping", host, rtt, perda, None, None)
        conn.commit()
    print("\n== Teste HTTP ==")
    for url in URLS:
        status, tempo = testar_http(url)
        print(f"{url} - Código: {status}, Tempo de carregamento: {tempo}")
        inserir_resultado(cur, "http", url, None, None, status, tempo)
        conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    wait_for_db()
    run_tests()
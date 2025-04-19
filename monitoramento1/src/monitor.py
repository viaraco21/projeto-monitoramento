import time
import requests
from ping3 import ping

# URLs para teste
URLS = ["https://google.com", "https://youtube.com", "https://rnt.br"]

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
    print("== Teste de Ping ==")
    for url in URLS:
        host = url.replace("https://", "").replace("http://", "").split("/")[0]
        rtt, perda = testar_ping(host)
        print(f"{host}: RTT médio = {rtt:.2f}ms, Perda = {perda:.1f}%")
    print("\n== Teste HTTP ==")
    for url in URLS:
        status, tempo = testar_http(url)
        print(f"{url} - Código: {status}, Tempo de carregamento: {tempo:.2f}s" if tempo else f"{url} - Erro: {status}")

if __name__ == "__main__":
    run_tests()

import requests
import time
import sys
from datetime import datetime

SERVER_URL = "http://web-server:8080"
INTERVAL_SECONDS = 5

def make_request():
    try:
        response = requests.get(SERVER_URL, timeout=3)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if response.status_code == 200:
            data = response.json()
            print(f"[{timestamp}] ✓ Sucesso - Requisição #{data.get('request_number')}")
            print(f"    Servidor: {data.get('hostname')}")
            print(f"    Mensagem: {data.get('message')}")
            print(f"    Status: {data.get('status')}")
        else:
            print(f"[{timestamp}] ✗ Erro - Status Code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✗ Erro de conexão com o servidor")
    except requests.exceptions.Timeout:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✗ Timeout na requisição")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✗ Erro: {str(e)}")

def main():
    print("="*60)
    print("Cliente HTTP - Requisições Periódicas")
    print(f"Servidor alvo: {SERVER_URL}")
    print(f"Intervalo: {INTERVAL_SECONDS} segundos")
    print("="*60)
    print()
    
    while True:
        make_request()
        print(f"    Aguardando {INTERVAL_SECONDS} segundos...\n")
        time.sleep(INTERVAL_SECONDS)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCliente encerrado pelo usuário.")
        sys.exit(0)

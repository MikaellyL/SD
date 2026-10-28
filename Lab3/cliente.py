import socket 
import threading
import sys
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8000

def receber_mensagens(cliente_socket):
    while True:
        try:
            mensagem = cliente_socket.recv(1024).decode('utf-8')
            if not mensagem:
                print("\n[DESCONECTADO] O servidor encerrou a conexão.")
                break

            # Imprime a mensagem recebida em uma nova linha e redefine o prompt '> '
            print(f"\n{mensagem}")
            print("> ", end="", flush=True)
        except Exception:
            break

    cliente_socket.close()

def iniciar_cliente():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente_socket.connect((HOST, PORT))
        print(f"[{datetime.now()}] Conectado ao servidor em {HOST}:{PORT}")
        print("Digite suas mensagens. Para sair, digite 'sair'.\n")
    except Exception as e:
        print(f"[{datetime.now()}] Erro ao conectar ao servidor: {e}")
        return

    thread_receber = threading.Thread(target=receber_mensagens, args=(cliente_socket,))
    thread_receber.start()

    try:
        while True:
            mensagem = input("> ")
            if mensagem.strip().lower() == "sair":
                print(f"[{datetime.now()}] Encerrando conexão com o servidor.")
                break
            if mensagem.strip():
                cliente_socket.sendall(mensagem.encode('utf-8'))
                
    except Exception as e:
        print(f"Erro ao enviar: {e}")
    finally:
        cliente_socket.close()
        sys.exit()

if __name__ == "__main__":
    iniciar_cliente()
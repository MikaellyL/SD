import socket 
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 8000 

# lista para armazenar os clientes conectados
clientes_conectados = []
# lock para evitar condições de corrida ao acessar a lista de clientes
lock_clientes = threading.Lock()

def broadcast_mensagem(mensagem, remetente):
    with lock_clientes:
        for cliente in clientes_conectados:
            if cliente != remetente:
                try:
                    cliente.sendall(mensagem.encode('utf-8'))
                except Exception as e:
                    print(f"[{datetime.now()}] Erro ao enviar mensagem para um cliente: {e}")

def tratar_cliente(cliente_socket, endereco):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Novo cliente conectado: {endereco}")
    with lock_clientes:
        clientes_conectados.append(cliente_socket)
    
    try:
        while True:
            mensagem = cliente_socket.recv(1024).decode()
            if not mensagem:
                break
            print(f"[{datetime.now()}] Mensagem recebida de {endereco}: {mensagem}")
            broadcast_mensagem(mensagem, remetente=cliente_socket)
    except Exception as e:
        print(f"[{datetime.now()}] Erro ao tratar cliente {endereco}: {e}")
    finally:
        # Remove o cliente e fecha a conexão com segurança
        with lock_clientes:
            clientes_conectados.remove(cliente_socket)
        cliente_socket.close()
        
        print(f"[{datetime.now()}] Cliente desconectado: {endereco}")   
        broadcast_mensagem(f"Cliente {endereco} desconectado.", remetente=None)

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reutilizar a porta imediatamente ao reiniciar o script
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[{datetime.now()}] Servidor iniciado em {HOST}:{PORT}")

    try:
        while True:
            cliente_socket, endereco = servidor.accept()
            thread_cliente = threading.Thread(target=tratar_cliente, args=(cliente_socket, endereco))
            thread_cliente.start()
    except KeyboardInterrupt:
        print(f"[{datetime.now()}] Servidor encerrado manualmente.")
    finally:
        servidor.close()   

if __name__ == "__main__":
    iniciar_servidor()           
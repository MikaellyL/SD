import socket 
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 8000   # Localhost

def tratar_cliente (conexao, endereco):
    print(f"[{datetime.now()}] Cliente conectado de {endereco}")

    try:
        data = conexao.recv(1024)
        if data: 
            mensagem = data.decode('utf-8')
            print(f"[{datetime.now()}] Mensagem recebida de {endereco}: {mensagem}")

            mensagem_revertida = mensagem[::-1]
            
            # 2. Obter o horário atual no servidor
            horario_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Formata a resposta com a string invertida e o horário
            resposta = f"String invertida: {mensagem_revertida} | Horário do Servidor: {horario_atual}"
            
            # Envia a resposta de volta ao cliente
            conexao.sendall(resposta.encode('utf-8'))
    except Exception as e:
        print(f"[ERRO] Falha na comunicação com {endereco}: {e}")
    finally:
        conexao.close()
        print(f"[CONEXÃO ENCERRADA] {endereco}")

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[AGUARDANDO] Servidor escutando em {HOST}:{PORT}...")
    
    while True:
        conexao, endereco = servidor.accept()
        # Cria e inicia uma nova thread para o cliente
        thread = threading.Thread(target=tratar_cliente, args=(conexao, endereco))
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()
import socket 

HOST = '127.0.0.1'
PORT = 8000   # Localhost

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        cliente.connect((HOST, PORT))

        mensagem = "olá, Mundo distribuido"
        print(f"[ENVIANDO]{mensagem}")

        cliente.sendall(mensagem.encode('utf-8'))
        
        resposta = cliente.recv(1024).decode('utf-8')
        print(f"[RESPOSTA DO SERVIDOR] {resposta}")
        
    except ConnectionRefusedError:
        print("[ERRO] Não foi possível conectar ao servidor. Verifique se ele está rodando.")
    finally:
        cliente.close()
        print("[ENCERRADO] Conexão finalizada.")

if __name__ == "__main__":
    iniciar_cliente()
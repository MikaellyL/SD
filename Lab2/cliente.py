import rpyc

HOST = '127.0.0.1'
PORT = 8000   # Localhost

def iniciar_cliente():
    try:
        # Conectar ao servidor RPyC
        conn = rpyc.connect(HOST, PORT)
        print(f"Conectado ao servidor RPyC em {HOST}:{PORT}")

        # Solicitar o horário atual do servidor
        horario_atual = conn.root.obter_horario()
        print(f"Horário atual do servidor: {horario_atual}")

    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")

    finally:
        # Fechar a conexão
        if 'conn' in locals():
            conn.close()
            print("Conexão encerrada.")
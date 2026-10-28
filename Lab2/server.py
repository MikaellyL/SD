
import rpyc
from rpyc.utils.server import ThreadedServer
from datetime import datetime

class HorarioService (rpyc.Service):
    def on_connect(self, conn):
        print("Client connected:", conn)

    def on_disconnect(self, conn):
        print("Client disconnected:", conn)

    def exposed_obter_horario(self):
        horario_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{datetime.now()}] Horário atual solicitado: {horario_atual}")
        return horario_atual

if __name__ == "__main__":
    PORT = 8000
    servidor = ThreadedServer(HorarioService, port=PORT)
    print(f"[{datetime.now()}] Servidor RPyC iniciado na porta {PORT}. Aguardando conexões...")
    servidor.start()
import socket
import threading
import asyncio
import websockets
import paho.mqtt.client as mqtt

HOST = "0.0.0.0"
TCP_PORT = 65432
WS_PORT = 8765

# Configurações MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensors/pot"
MQTT_USER = "projeto"
MQTT_PASS = "proj"

ultimo_valor = None
clients = set()


# --- TCP (ESP32) ---
def handle_esp32(conn, addr):
    global ultimo_valor
    print(f"[TCP] Nova conexão de {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"[TCP] Conexão encerrada por {addr}")
                break
            ultimo_valor = data.decode().strip()
            print(f"[TCP] Recebido de {addr}: {ultimo_valor}")


def inicia_servidor_tcp():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, TCP_PORT))
        s.listen()
        print(f"[TCP] Servidor ouvindo em {HOST}:{TCP_PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(
                target=handle_esp32, args=(conn, addr), daemon=True
            )
            thread.start()


# --- MQTT ---
def on_message(client, userdata, msg):
    global ultimo_valor
    ultimo_valor = msg.payload.decode()
    print(f"[MQTT] Recebido: {ultimo_valor}")


def inicia_mqtt():
    print(f"[MQTT] Servidor ouvindo em {MQTT_BROKER}:{MQTT_PORT}")
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.username_pw_set(MQTT_USER, MQTT_PASS)
        client.on_message = on_message
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.subscribe(MQTT_TOPIC)
        client.loop_start()
    except Exception as e:
        print(f"[MQTT] Erro: {e}")


# --- WebSocket (Frontend) ---
# Tanto o TCP quanto o MQTT usam o WebSocket para enviar informações
async def ws_handler(websocket):
    print("[WS] Cliente conectado")
    clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(0.5)
            if ultimo_valor is not None:
                await websocket.send(ultimo_valor)
    except websockets.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)
        print("[WS] Cliente desconectado")


async def inicia_servidor_websocket():
    print(f"[WS] Servidor WebSocket em ws://{HOST}:{WS_PORT}")
    async with websockets.serve(ws_handler, HOST, WS_PORT):
        await asyncio.Future()


# --- Main ---
def main():
    # Inicia MQTT
    inicia_mqtt()

    # Inicia servidor TCP em uma thread separada
    tcp_thread = threading.Thread(target=inicia_servidor_tcp, daemon=True)
    tcp_thread.start()

    # Inicia Websocket
    asyncio.run(inicia_servidor_websocket())


if __name__ == "__main__":
    main()

import socket
import threading
import asyncio
import websockets
import paho.mqtt.client as mqtt

HOST = '0.0.0.0'  # Listen on all interfaces
TCP_PORT = 65432
WS_PORT = 8765

# MQTT config
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPIC = 'sensors/pot'
MQTT_USER = 'projeto'
MQTT_PASS = 'proj'

latest_value = None
clients = set()

# --- TCP (ESP32) ---

def handle_esp32(conn, addr):
    global latest_value
    print(f"[TCP] Nova conexão de {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"[TCP] Conexão encerrada por {addr}")
                break
            latest_value = data.decode().strip()
            print(f"[TCP] Recebido de {addr}: {latest_value}")

def start_tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, TCP_PORT))
        s.listen()
        print(f"[TCP] Servidor ouvindo em {HOST}:{TCP_PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_esp32, args=(conn, addr), daemon=True)
            thread.start()

# --- MQTT ---

def on_message(client, userdata, msg):
    global latest_value
    latest_value = msg.payload.decode()
    print(f"[MQTT] Recebido: {latest_value}")

def start_mqtt():
    print(f"[MQTT] Servidor ouvindo em {MQTT_BROKER}:{MQTT_PORT}")
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.subscribe(MQTT_TOPIC)
    client.loop_start()

# --- WebSocket (Frontend) ---

async def ws_handler(websocket):
    print("[WS] Cliente conectado")
    clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(0.5)
            if latest_value is not None:
                await websocket.send(latest_value)
    except websockets.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)
        print("[WS] Cliente desconectado")

async def start_websocket_server():
    print(f"[WS] Servidor WebSocket em ws://{HOST}:{WS_PORT}")
    async with websockets.serve(ws_handler, HOST, WS_PORT):
        await asyncio.Future()

# --- Main ---

def main():
    # Start TCP in separate thread
    tcp_thread = threading.Thread(target=start_tcp_server, daemon=True)
    tcp_thread.start()

    # Start MQTT
    start_mqtt()

    # Start WebSocket loop
    asyncio.run(start_websocket_server())

if __name__ == "__main__":
    main()

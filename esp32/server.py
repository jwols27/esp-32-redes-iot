import socket
import threading
import asyncio
import websockets

HOST = '0.0.0.0'  # Listen on all interfaces for ESP32 + frontend
TCP_PORT = 65432
WS_PORT = 8765

latest_value = None
clients = set()

# TCP handler for ESP32
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

# Start TCP server
def start_tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, TCP_PORT))
        s.listen()
        print(f"[TCP] Servidor ouvindo em {HOST}:{TCP_PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_esp32, args=(conn, addr), daemon=True)
            thread.start()

# WebSocket handler for frontend
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

# Start WebSocket server
async def start_websocket_server():
    print(f"[WS] Servidor WebSocket em ws://{HOST}:{WS_PORT}")
    async with websockets.serve(ws_handler, HOST, WS_PORT):
        await asyncio.Future()  # run forever

# Run both TCP and WebSocket
def main():
    tcp_thread = threading.Thread(target=start_tcp_server, daemon=True)
    tcp_thread.start()
    asyncio.run(start_websocket_server())

if __name__ == "__main__":
    main()

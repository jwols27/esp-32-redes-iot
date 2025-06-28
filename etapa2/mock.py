import threading
import time
import random
import paho.mqtt.client as mqtt

# MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_USER = "projeto"
MQTT_PASS = "proj"
TOPICO_PREFIXO = "esp32"

mqtt_client = None
mqtt_lock = threading.Lock()


class MockADC:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        return random.randint(600, 1195)


class MockDS18B20:
    def __init__(self):
        self.roms = ["fake_rom"]

    def scan(self):
        return self.roms

    def convert_temp(self):
        time.sleep(1)

    def read_temp(self, rom):
        return round(random.uniform(20.0, 35.0), 2)


pino_umidade = MockADC(34)
ds = MockDS18B20()


def reconectar_mqtt():
    global mqtt_client
    with mqtt_lock:
        try:
            mqtt_client = mqtt.Client(
                client_id="esp32", callback_api_version=mqtt.CallbackAPIVersion.VERSION2
            )
            mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
            mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
            print("MQTT conectado.")
        except Exception as e:
            print("Erro ao conectar MQTT:", e)


def publicar(valor, topico: str):
    global mqtt_client
    topico_mqtt = f"{TOPICO_PREFIXO}/{topico}"
    try:
        with mqtt_lock:
            mqtt_client.publish(topico_mqtt, str(valor))
        print(f"{topico} -> {valor}")
    except Exception as e:
        print(f"Erro ao publicar em {topico_mqtt}: {e}")
        reconectar_mqtt()
        try:
            with mqtt_lock:
                mqtt_client.publish(topico_mqtt, str(valor))
        except Exception as e2:
            print(f"Falha após reconectar: {e2}")


def loop_temperatura():
    roms = ds.scan()
    if not roms:
        print("Nenhum sensor DS18B20 encontrado!")
        return
    rom = roms[0]

    while True:
        ds.convert_temp()
        temperatura = ds.read_temp(rom)
        publicar(temperatura, "temperatura")
        time.sleep(10)


def loop_umidade():
    while True:
        umidade = pino_umidade.read()
        publicar(umidade, "umidade")
        time.sleep(0.5)


def main():
    reconectar_mqtt()
    threading.Thread(target=loop_temperatura, daemon=True).start()
    loop_umidade()


if __name__ == "__main__":
    main()

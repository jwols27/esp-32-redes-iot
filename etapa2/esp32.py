import _thread
import network
from umqtt.simple import MQTTClient
from machine import ADC, Pin
import time
import onewire
import ds18x20

# Pinos
pino_umidade = ADC(Pin(34))
pino_umidade.atten(ADC.ATTN_11DB)

pino_temperatura = Pin(33)
ow = onewire.OneWire(pino_temperatura)
ds = ds18x20.DS18X20(ow)

# Wi-Fi
WIFI_SSID = "visitantes"
WIFI_PASS = ""

wlan = network.WLAN(network.STA_IF)

# MQTT
MQTT_BROKER = "172.20.165.147"
MQTT_PORT = 1883
MQTT_USER = "projeto"
MQTT_PASS = "proj"

TOPICO_PREFIXO = "esp32"

mqtt_client = None
mqtt_lock = _thread.allocate_lock()

def conectar_wifi():
    if not wlan.isconnected():
        print(f"Wi-Fi - Conectando na rede [{WIFI_SSID}]...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(0.5)
        print("\nWi-Fi conectado:", wlan.ifconfig())

def reconectar_mqtt():
    global mqtt_client
    with mqtt_lock:
        try:
            mqtt_client = MQTTClient("esp32", MQTT_BROKER, user=MQTT_USER, password=MQTT_PASS, port=MQTT_PORT)
            mqtt_client.connect()
            print("MQTT reconectado.")
        except Exception as e:
            print("Erro ao reconectar MQTT:", e)

def publicar(valor, topico: str):
    global mqtt_client
    topic = bytes(f"{TOPICO_PREFIXO}/{topico}", "utf-8")
    try:
        with mqtt_lock:
            mqtt_client.publish(topic, str(valor))
        print(f"{topico} -> {valor}")
    except OSError:
        print("Erro de conexão MQTT. Tentando reconectar...")
        reconectar_mqtt()
        try:
            with mqtt_lock:
                mqtt_client.publish(topic, str(valor))
        except Exception as e:
            print(f"Falha ao publicar {topico} após reconectar: {e}")
    except Exception as e:
        print(f"Falha ao publicar {topico}: {e}")

def loop_temperatura():
    roms = ds.scan()
    if not roms:
        print("Nenhum sensor DS18B20 encontrado!")
        return
    rom = roms[0]

    while True:
        if not wlan.isconnected():
            print("Wi-Fi (temperatura) desconectado. Reconectando...")
            conectar_wifi()
            reconectar_mqtt()

        ds.convert_temp()
        time.sleep(10)
        temperatura = ds.read_temp(rom)
        publicar(temperatura, "temperatura")
        time.sleep(1)

def loop_umidade():
    while True:
        if not wlan.isconnected():
            print("Wi-Fi (umidade) desconectado. Reconectando...")
            conectar_wifi()
            reconectar_mqtt()

        umidade = pino_umidade.read()
        publicar(umidade, "umidade")
        time.sleep(0.5)

def main():
    wlan.active(True)
    conectar_wifi()
    reconectar_mqtt()

    _thread.start_new_thread(loop_temperatura, ())
    loop_umidade()

main()


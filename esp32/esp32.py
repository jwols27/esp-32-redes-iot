import _thread
import network
from umqtt.simple import MQTTClient
from machine import ADC, Pin
import time

pino_umidade = ADC(Pin(34))
pino_umidade.atten(ADC.ATTN_11DB)

WIFI_SSID = "visitantes"
WIFI_PASS = ""

MQTT_BROKER = "172.20.163.175"
MQTT_PORT = 1883
MQTT_USER = "projeto"
MQTT_PASS = "proj"

TOPICO_PREFIXO = "esp32"

def conectar_wifi(wlan):
    print(f"Wi-Fi - Conectando na rede [{WIFI_SSID}]...")
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        print(".")
        time.sleep(0.5)
    print("Wi-Fi conectado:", wlan.ifconfig())

def publicar(client: MQTTClient, valor, topico: str):
    topic = bytes(f"{TOPICO_PREFIXO}/{topico}", "utf-8")
    try:
        client.publish(topic, str(valor))
        print(f"{topico.capitalize()} -> {valor}")
    except OSError:
        print("Conexão MQTT perdida, reconectando...")
        try:
            client.connect()
            client.publish(topic, str(valor))
        except Exception as e:
            print(f"Falha ao reconectar e publicar {topico}: {e}")
    except Exception as e:
        print(f"Falha ao publicar {topico}: {e}")

def publicar_temperatura():
    client = MQTTClient("esp32_temp", MQTT_BROKER, user=MQTT_USER, password=MQTT_PASS, port=MQTT_PORT)
    client.connect()
    while True:
        temperatura = 0  # ler_sensor()
        publicar(client, temperatura, "temperatura")
        time.sleep(10)

def publicar_umidade(wlan):
    client = MQTTClient("esp32_umid", MQTT_BROKER, user=MQTT_USER, password=MQTT_PASS, port=MQTT_PORT)
    client.connect()

    while True:
        if not wlan.isconnected():
            print("Conexão Wi-Fi perdida.")
            conectar_wifi(wlan)

        umidade = pino_umidade.read()
        publicar(client, umidade, "umidade")
        time.sleep(0.1)

def main():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    conectar_wifi(wlan)

    _thread.start_new_thread(publicar_temperatura, ())
    publicar_umidade(wlan)

main()

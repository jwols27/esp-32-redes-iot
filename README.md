##  ESP32

### Escolha 1 - C
Rode o arquivo [`esp32.ino`](./etapa1/esp32.ino), com Arduino IDE por exemplo.

A ESP32 tentará se conectar a uma rede Wi-Fi e então ao MQTT, mas se não conseguir se conectar ao MQTT se conectará ao servidor HTTP especificado.

### Escolha 2 - MicroPython
Rode o arquivo [`esp32.py`](./etapa2/esp32.py), com Thonny por exemplo.

A ESP32 tentará se conectar ao MQTT depois de se conectar a uma rede Wi-Fi.

##  MQTT

Suba o MQTT com usuário/senha projeto:proj na porta 1883.

## Middleware

###  Websocket
Inicie o [`server.py`](./etapa1/server/server.py). Ele se conectará automaticamente ao MQTT local.

O servidor também iniciará um servidor TCP.

### Node-RED

Inicie o Node-RED e importe o arquivo [`flows.json`](./etapa2/flows.json). Não esqueca de preencher os dados de autenticação.

## Svelte

Use somente se você abrir o Websocket.

Coloque sua chave WeatherAPI num arquivo `.env` como WEATHER_API_KEY.

Execute o comando abaixo para subir o site.

```bash
npm run dev
```

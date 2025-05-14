#  ESP32

Rode o arquivo `esp32.ino`, com Arduino IDE por exemplo.

A ESP32 tentará se conectar ao MQTT, mas se não conseguir se conectará ao servidor HTTP especificado.

#  MQTT

Suba o MQTT com usuário/senha projeto:proj.

#  Websocket

Inicie o `server.py`. Ele se conectará automaticamente ao MQTT local.

O servidor também iniciará um servidor TCP.

# Frontend

Coloque sua chave WeatherAPI num arquivo `.env` como WEATHER_API_KEY.

Rode o comando abaixo para subir o site.

```bash
npm run dev
```

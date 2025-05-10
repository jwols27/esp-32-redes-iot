#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Ana";           // Nome da rede WiFi
const char* password = "98126124";  // Senha da rede WiFi

const char* serverAddress = "192.168.119.9";    // Endereço IP do servidor
const int serverPort = 65432;                   // Porta do servidor

const char* mqtt_server = serverAddress;    // IP do broker MQTT

// MQTT credentials
const char* mqtt_user = "projeto";
const char* mqtt_pass = "proj";

const int potPin = 34;
int potValue = 0;

WiFiClient client;
WiFiClient mqttClient;
PubSubClient mosClient(mqttClient);

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensagem recebida [");
  Serial.print(topic);
  Serial.print("] ");
  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void conectarMQTT() {
  Serial.println("Conectando ao MQTT...");
  if (mosClient.connect("ESP32Client", mqtt_user, mqtt_pass)) {
    Serial.println("MQTT Conectado!");
  } else {
    Serial.print("Falha na conexão MQTT! rc=");
    Serial.print(mosClient.state());
  }
}

bool conectarHTTP() {
  if (!client.connected()) {
    client.stop();
    
    // Tenta conectar ao servidor
    Serial.println("Conectando ao servidor HTTP...");
    if (client.connect(serverAddress, serverPort)) {
      Serial.println("HTTP Conectado!");
      return true;
    } 
    else {
      Serial.println("Falha na conexão HTTP!");
      delay(100);
      return false;
    }
  } else {
    Serial.print("Conectado ao servidor HTTP: ");
    Serial.println(serverAddress);
    return true;
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.print("Conectando à rede WiFi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi conectado!");
  Serial.print("Endereço IP: ");
  Serial.println(WiFi.localIP());

  mosClient.setServer(mqtt_server, 1883);
  mosClient.setCallback(callback);
  Serial.println("Coletando umidade...");
}

void loop() {
  potValue = 0;
  for(int i = 0; i < 25; i++) {
    potValue += analogRead(potPin);
    delay(200);
  }

  bool conectado = mosClient.connected() || client.connected();
  while(!conectado) {
    if (!mosClient.connected()) {
      conectarMQTT();
    } else {
      conectado = true;
    }
    if (!conectado) {
      conectado = conectarHTTP();
    }
  }

  Serial.println(potValue / 25);

  if (mosClient.connected()) {
    char msg[10];
    snprintf(msg, sizeof(msg), "%d", potValue / 25);
    mosClient.publish("sensors/pot", msg);
  }

  if (client.connected()) {
    client.println(potValue / 25);
  }

  mosClient.loop();
}

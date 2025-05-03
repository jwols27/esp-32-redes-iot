#include <WiFi.h>

const char* ssid = "Ana";   // Nome da rede WiFi
const char* password = "98126124";    // Senha da rede WiFi

const char* serverAddress = "192.168.40.9";  // Endereço IP do servidor
const int serverPort = 65432;                 // Porta do servidor

const int potPin = 34;

int potValue = 0;

WiFiClient client;

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

  Serial.print("Conectando ao servidor: ");
  Serial.println(serverAddress);
  
  if (client.connect(serverAddress, serverPort)) {
    Serial.println("Conectado ao servidor com sucesso!");
    
    // Envia a mensagem "oi" para o servidor
    client.println("oi");
    Serial.println("Mensagem enviada: oi");
  } 
  else {
    Serial.println("Falha na conexão com o servidor!");
  }
}

void loop() {
  potValue = analogRead(potPin);
  Serial.println(potValue);

  if (!client.connected()) {
    Serial.println("Conexão com o servidor perdida");
    client.stop();
    
    // Aguarda um tempo antes de tentar reconectar
    delay(5000);
    
    // Tenta reconectar ao servidor
    Serial.print("Reconectando ao servidor...");
    if (client.connect(serverAddress, serverPort)) {
      Serial.println("Conectado!");
      client.println("oi");
      Serial.println("Mensagem enviada: oi");
    } 
    else {
      Serial.println("Falha na reconexão!");
      delay(100);
      return;
    }
  }

  client.print(potValue);
  delay(500);
}

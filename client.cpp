#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "p24i01";
const char* password = "";

const char* serverIP = "192.168.10.1";
const int serverPort = 12345;

WiFiUDP udp;
int msg = 0;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Łączenie...");
  }

  Serial.print("Połączono, IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  udp.beginPacket(serverIP, serverPort);
  udp.printf("hello, nr: %d", msg);
  udp.endPacket();

  msg++;

  int len = udp.parsePacket();
  if (len) {
    char buf[256];
    int n = udp.read(buf, 256);
    buf[n] = '\0';
    Serial.println(buf);
  }

  delay(1000);
}



#include "Include_Lib.h"
#include "MQTT_Alert_Client.h"


// DMX
// Instanz für DMXausgabe
DMXESPSerial myDMX;
uint8_t DMXValue1 = 9;      //number for red
uint8_t DMXValue2 = 0;



void alertCallback(char* x, uint16_t len) {
    Serial.print("value: ");
    Serial.println(x);
    myDMX.write(1, DMXValue1);
    myDMX.write(2, DMXValue2);
    myDMX.update();
    delay(1);
}


void setup() {

    //Setup UART connection
    //Serial.begin(9600);

    //Setup WiFi connection
    //Serial.print("Connecting to WLAN");
    initWiFi();         //func. declaration: MQTT_Client_Config.h
    myAlert.setCallback(alertCallback);
    myMqtt.subscribe(&myAlert);
    myDMX.init(32);     // 32 Channels
}



void loop() {
    // Ensure the connection to the MQTT server is alive (this will make the first
    // connection and automatically reconnect when disconnected).  See the MQTT_connect
    // function definition further below.
    MQTT_connect();
    // this is our 'wait for incoming subscription packets and callback em' busy subloop
    myMqtt.processPackets(1000);
}
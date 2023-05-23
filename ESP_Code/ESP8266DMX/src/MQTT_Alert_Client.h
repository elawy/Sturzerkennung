
#include "Include_Lib.h"

//HardwareSerial printSerial = Serial1;
/************************* WiFi Access Point *********************************/
#define WLAN_SSID       "xxxxx"
#define WLAN_PASS       "xxxxx"

/************************* Adafruit.io Setup *********************************/
#define AIO_SERVER      "xxx.xxx.xxx.xx"   //IP-Adress from Raspberry Pi
#define AIO_SERVERPORT  1883                  
#define AIO_USERNAME    "xxxx"
#define AIO_KEY         "xxxx"

/************************** Global State ************************************/

// Create an ESP8266 WiFiClient class to connect to the MQTT server.
WiFiClient client;
// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
Adafruit_MQTT_Client myMqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

/****************************** Feeds ***************************************/

// Setup a feed called 'test' for subscribing to changes.
Adafruit_MQTT_Subscribe myAlert = Adafruit_MQTT_Subscribe(&myMqtt, AIO_USERNAME "/alert");

/***************************Declared functions*********************************/
void initWiFi();        //Init WiFi connection
void MQTT_connect();

/****************************** Functions ***************************************/
void initWiFi() {
    WiFi.begin(WLAN_SSID, WLAN_PASS);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        //printSerial.print(".");
    }
    // printSerial.println();
    // printSerial.println("WiFi connected");
    // printSerial.println("IP address: "); 
    // printSerial.println(WiFi.localIP());
}

// Function to connect and reconnect as necessary to the MQTT server.
// Should be called in the loop function and it will take care if connecting.
void MQTT_connect() {
  int8_t ret;

  // Stop if already connected.
  if (myMqtt.connected()) {
    return;
  }

  //printSerial.print("Connecting to MQTT... ");

  uint8_t retries = 3;
  while ((ret = myMqtt.connect()) != 0) { // connect will return 0 for connected
    //    printSerial.println(myMqtt.connectErrorString(ret));
    //    printSerial.println("Retrying MQTT connection in 5 seconds...");
       myMqtt.disconnect();
       delay(5000);  // wait 5 seconds
       retries--;
       if (retries == 0) {
         // basically die and wait for WDT to reset me
         while (1);
       }
    }
//printSerial.println("MQTT Connected!");
}

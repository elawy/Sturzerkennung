#include "Include_Lib.h"

//WiFi Access Point
#define WLAN_SSID       "xxxx"
#define WLAN_PASS       "xxxx"

//MQTT Broker
#define AIO_SERVER      "xxx.xxx.xxx.xx"   //IP-Adress from Raspberry Pi
#define AIO_SERVERPORT  1883                  
#define AIO_USERNAME    "xxxx"
#define AIO_KEY         "xxxx"

//ESP8266 WiFiClient class
WiFiClient client;

//MQTT Client
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

Adafruit_MQTT_Publish esp8266_dps310_temperature = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/ESP8266/Ref/DPS310/Temperature", MQTT_QOS_1);
Adafruit_MQTT_Publish esp8266_dps310_pressure = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/ESP8266/Ref/DPS310/Pressure", MQTT_QOS_1);
Adafruit_MQTT_Publish esp8266_dps310_compensated_pressure = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/ESP8266/Ref/DPS310/CompensatedPressure", MQTT_QOS_1);

//Declared functions
void initWiFi();        //Init WiFi connection
void MQTT_connect();    //Connect MQTT Broker

//Functions
void initWiFi() {
    WiFi.begin(WLAN_SSID, WLAN_PASS);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println();
    Serial.println("WiFi connected");
    Serial.println("IP address: "); Serial.println(WiFi.localIP());
}

void MQTT_connect(){
    if (mqtt.connected()) 
        {
            //Serial.println("MQTT Connected");
            return;
        }

    while ((mqtt.connect()) != 0)               // mqtt.connect() will return 0 for connected
        { 
        Serial.println("MQTT not connected");
        // While mqtt is not connected... 
        mqtt.disconnect();                     // Disconnect from MQTT-Server
        if(WiFi.status() != WL_CONNECTED)      // Check if WiFi is connected      
            {
                Serial.println("Connect Wifi");
                // if WiFi is not connected...
                // WiFi.disconnect();                // Disconnect from WiFi-network
                // WiFi.begin(WLAN_SSID, WLAN_PASS); // Connect to WiFi-network
                // delay(2000);                      // Wait 2 sec in order to establish WiFi-connection 
                initWiFi();  
            }
        else
            {
                Serial.println("Wifi connected");
                delay(2000);                      // wait 2 seconds in order to establish MQTT-connection  
            }   
        }
  }

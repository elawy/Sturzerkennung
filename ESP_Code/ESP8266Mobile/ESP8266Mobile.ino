//#include <Include_Lib.h>

extern "C" {
#include "user_interface.h"
}

#include <Dps310.h>
#include <ESP8266WiFi.h>
#include <Adafruit_MQTT.h>
#include <Adafruit_MQTT_Client.h>

//MQTT Configuration
#include "MQTT_Client_Config.h"

//DPS310 Configuration
#include "DPS310_Config.h"

void setup() {
  //Setup UART connection
  Serial.begin(9600);
  
  //Setup WiFi connection
  initWiFi();     //func. declaration: MQTT_Client_Config.h
 
  //Setup I2C connection with DPS310
  Dps310PressureSensor.init();      //func. declaration: Dps310.cpp
  //I2C begin function for Dps310 with standard address
  Dps310PressureSensor.begin(Wire); //func. declaration: Dps310.cpp
}

void loop() {
  MQTT_connect();
  int16_t ret = Dps310PressureSensor.measurePressureOnce(pressure, prs_osr);   //func. declaration: Dps310.cpp

  if (ret != 0)
  {
    //Something went wrong.
    //Look at the library code for more information about return codes
    Serial.print("FAIL! ret = ");
    Serial.println(ret);
  }
  else
  {
    Serial.print("Pressure: ");
    Serial.print(pressure,10);
    Serial.print(" Pascal ");
    esp8266_dps310_pressure.publish(Dps310PressureSensor.pressure_d);
  }

  ret = Dps310PressureSensor.measureTempOnce(temperature, temp_osr);

  if (ret != 0)
  {
    //Something went wrong.
    //Look at the library code for more information about return codes
    Serial.print("FAIL! ret = ");
    Serial.println(ret);
  }
  else
  {
    Serial.print("Temperature: ");
    Serial.print(temperature,10);
    Serial.println(" degrees of Celsius");
    esp8266_dps310_temperature.publish(Dps310PressureSensor.temperature_d);
  }
}

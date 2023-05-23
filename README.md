# Sturzerkennung
Demoanwendung eines Sturzerkennungssystems

## Aufbau der Hardware

Der Sensor DPS310 ist über Kabel mit dem µC ESP8266 verbunden. Die Kommunikation findet über 
die Schnittstelle I2C statt. Über die Arduino IDE Software oder PlatformIO wird der 
Code auf den µC ESP8266 geladen. Der µC kommuniziert kabellos über das Protokoll MQTT mit dem 
Raspberry Pi. Dies erfolgt über das Lokale Netzwerk. Auf dem 
Raspberry Pi ist der MQTT-Broker Mosquitto, die Datenbank MariaDB sowie die Monitoring Software 
Grafana installiert. Die Daten werden über den MQTT-Broker an ein Python Skript übermittelt. Das 
Skript empfängt die Daten, berechnet den Höhenunterschied und speichert diese in der Datenbank
MariaDB ab. Grafana kann über jedes Endgerät, das sich im gleichen Netzwerk befindet, aufgerufen 
werden. Über diesen können die Daten graphisch visualisiert werden.

<img src= "https://github.com/elawy/Sturzerkennung/assets/48498386/3145d010-5858-460b-a5b0-72b362cbb52f" width= 500 hight= 450> 

## Berechnung
### Barometrische Höhenformel
Anhand der Temperatur- und Druckwerte beider Sensoren kann die relative Höhe zwischen den beiden 
Sensoren berechnet werden. Der Druck der Luft wird durch das Gewicht der Erdatmosphäre verursacht. 
Daraus folgt, dass der Luftdruck mit zunehmender Höhe fällt, wodurch das negative Vorzeichen in der 
Formel entsteht. Dies kann im späteren mit der Monitoring Software Grafana, die in diesem Projekt 
verwendet wird, nachvollzogen werden. Für die barometrische Höhenformel werden vereinfachte 
Annahmen gemacht. Zum einen, dass der Luftdruck mit der Höhe exponentiell abnimmt und zum 
anderen das die Temperatur immer gleichbleibt. Aus diesem Grund wird auch der Mittelwert der beiden 
Temperaturwerte für die Berechnung verwendet [https://math24.net/barometric-formula.html].

<img src = "https://github.com/elawy/Sturzerkennung/assets/48498386/19ef7a9a-5ae5-4b0a-9930-5718fb7ffa00" width= 500 hight= 450>

### Offsetberechnung
Vor der Nutzung des Sturzerkennungssystems müssen die Sensoren kalibriert werden, um Versatzfehler
auszugleichen. Dafür werden beide Sensoren nebeneinandergelegt. Wenn das System gestartet wird, 
beginnt die Berechnung des Offsetwertes über 10 Sekunden. In dieser Zeit werden die Druckwerte 
beider Sensoren gesammelt. Nach den 10 Sekunden werden die Mittelwerte des Mobilen- und 
Referenzsensors berechnet und in die folgende Formel eingesetzt:

<img src= "https://github.com/elawy/Sturzerkennung/assets/48498386/23fa7729-5ccc-4f3a-94d9-1dd388344c62" width= 300 hight= 250>

Nach Berechnung des Offsetwertes, wird diese in die oben aufgeführte barometrische Höhenformel 
implementiert. Dies sieht im Anschluss wie folgt aus:

<img src= "https://github.com/elawy/Sturzerkennung/assets/48498386/669a89e1-a8be-419b-b45e-e59fbb3fe60f" width= 300 hight= 250>

## SQL
Datensatz einer Sekunde
<img src= "https://github.com/elawy/Sturzerkennung/assets/48498386/f19417c2-f8a6-499f-ae85-37ae56e0d40b" width= 8000 hight= 150>

## Analyse mit Grafana
### Bezug zwischen Höhe und Druck

An Hand der folgenden Abbildung ist der Bezug zwischen Druck und Höhe nachzuvollziehen. Wenn der Mobile Sensor 
sich nach unten bewegt erhöhen sich die Druckwerte. Im zweiten Abschnitt ist genau das Gegenteil zu erkennen. Wenn sich der Sensor 
nach oben bewegt fallen die Druckwerte. Die Temperaturwerte bleiben bei beiden Sensoren konstant. 
Der blaue Graph ist der Mittelwert beider Temperaturwerte mit dem die Höhendifferenz ermittelt wird.

<img src = "https://github.com/elawy/Sturzerkennung/assets/48498386/d39b8f07-954a-4cf2-a58c-0ff649aaa542" width= 600 hight= 800>


#!/usr/bin/env python
# coding: utf-8


# Date:         19.02.2020 (last update)
# Author:       Miriam Nold
# Project:      Demoanwendung des Sturzerkennungssystems
# Description:  This Code saves the Data in the database. First it
#				subscribes the Pressure and Temperature Topics from
#				the Mobile and the Reference Sensor. After that it
#				calculates with the offset value the height sheid.
#				At the end it saves all the data in the database.

import paho.mqtt.client as mqtt
import MySQLdb
import time
import math

#Open database connection:
myDB = MySQLdb.connect("localhost","nold","futureaging","ESP_Data")
myCursor = myDB.cursor()

# variables wehre the data will pe save temporarly
pressureData_Mobile = ""
temperatureData_Mobile = ""
pressureData_Ref = ""
temperatureData_Ref = ""
offset = 0.0

# subscriptions to topics
def on_connect(client, userdata, flags, rc):

	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("openhabian/ESP8266/Mobile/DPS310/Pressure")
	client.subscribe("openhabian/ESP8266/Mobile/DPS310/Temperature")
        client.subscribe("openhabian/ESP8266/Ref/DPS310/Pressure")
        client.subscribe("openhabian/ESP8266/Ref/DPS310/Temperature")

	# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
#	print(msg.topic+" "+str(msg.payload))
	# devine the global variables, so that the data will be saved even
	# until all divrend data are insert into the databank
	global pressureData_Mobile
	global temperatureData_Mobile
	global pressureData_Ref
	global temperatureData_Ref

        if msg.topic == "openhabian/ESP8266/Mobile/DPS310/Pressure":
		pressureData_Mobile = msg.payload
#		print(pressureData_Mobile)

        elif msg.topic == "openhabian/ESP8266/Mobile/DPS310/Temperature":
		temperatureData_Mobile = msg.payload
#		print(temperatureData_Mobile)

        elif msg.topic == "openhabian/ESP8266/Ref/DPS310/Pressure":
		pressureData_Ref = msg.payload
#               print(pressureData_Ref)

        elif msg.topic == "openhabian/ESP8266/Ref/DPS310/Temperature":
                temperatureData_Ref = msg.payload
#               print(temperatureData_Ref)
	# check if all divrent kind of data arrived yet
	if pressureData_Mobile.strip()\
		 and temperatureData_Mobile.strip()\
		 and pressureData_Ref.strip()\
		 and temperatureData_Ref.strip():

		# calculation of the delta High value
		temp = -((float(temperatureData_Mobile) + float(temperatureData_Ref))/2 + 273.15)/0.0341593
		deltaHigh_without = temp * math.log(float(pressureData_Mobile)/float(pressureData_Ref)) * 1000
#		print ("deltaHigh_without", deltaHigh_without)

                tempPressMo = float(pressureData_Mobile) + offset
                tempPressRe = float(pressureData_Ref) - offset
		deltaHigh_with = temp * math.log(tempPressMo / tempPressRe) * 1000
#		print ("deltaHigh_with", deltaHigh_with)

		# insert data in databank
		myCursor.execute("""INSERT INTO SensorData\
		 (Pressure_Mobile, Temperature_Mobile, Pressure_Ref, Temperature_Ref,\
		 deltaHigh_without_Offset, deltaHigh_with_Offset)\
		 VALUES (%s, %s, %s, %s, %s, %s)""",\
		 (pressureData_Mobile, temperatureData_Mobile, pressureData_Ref, temperatureData_Ref,\
		 deltaHigh_without, deltaHigh_with,))
                myDB.commit()

#		print("Insert into Databank")

		# delte data in variable so the new block can be saved
		pressureData_Mobile = ""
		temperatureData_Mobile = ""
		pressureData_Ref = ""
		temperatureData_Ref = ""
def start(temp):
#	print("im databaseSaver : " + str(temp))
	global offset
	offset = temp
	myClient = mqtt.Client()
	myClient.on_connect = on_connect
	myClient.on_message = on_message
	myClient.connect('localhost')
	myClient.subscribe("openhabian/#")


	myClient.loop_start()
	# after 10*60s the skrpit will stopp automatically
	time.sleep(10*60)
	myClient.loop_stop()

	myDB.close()


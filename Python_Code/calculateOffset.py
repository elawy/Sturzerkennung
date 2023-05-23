# Date:         19.02.2020 (last update)
# Author:       Miriam Nold
# Project:      Demoanwendung des Sturzerkennungssystems
# Description:	This Code calculates the Offset Value. It subscribes
#				the Pressure Topics from the Mobile and the Reference
#				Sensor over 10 seconds. After that it calculates the
#				Offset Value and returned it to the main code.


import paho.mqtt.client as mqtt
import time

# global lists to collect enough data for the average
pressureMobileList=[]
pressureRefList= []

# The callback for when the client receives a CONNACK response from the server.
# Called when the broker responds to our connection request.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	myClient.subscribe("openhabian/ESP8266/Mobile/DPS310/Pressure")
	myClient.subscribe("openhabian/ESP8266/Ref/DPS310/Pressure")

# The callback for when a PUBLISH message is received from the server.
# Called when a message has been received on a topic that the client
# subscribes to and the message does not match an existing topic filter callback.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	global pressureMobileList
	global pressureRefList
	if msg.topic == "openhabian/ESP8266/Mobile/DPS310/Pressure":
		pressureMobileList.append(float(msg.payload))
	elif msg.topic == "openhabian/ESP8266/Ref/DPS310/Pressure":
		pressureRefList.append(float(msg.payload))
		print(msg.topic+" "+str(msg.payload))

def offset_Calculation():
	global pressureMobileList
	global pressureRefList
	# calculate the average from the Mobile and Reference Pressure Value
	pressureAveMo = sum(pressureMobileList) / len(pressureMobileList)
	pressureAveRef= sum(pressureRefList) / len(pressureRefList)
	offset = (pressureAveRef - pressureAveMo) / 2
	print ("aveMob: " + str(pressureAveMo))
	print("averReferenz: " + str(pressureAveRef))
	print ("Offset: " + str(offset))
	print ("Calculate over " + str(len(pressureMobileList)) + "values")
	return offset

def start():
	# Create a client instance with the name myClient
	myClient = mqtt.Client()
	myClient.on_connect = on_connect
	myClient.on_message = on_message

	myClient.connect('localhost')	# connect to broker
	myClient.subscribe("openhabian/ESP8266/Mobile/DPS310/Pressure")
	myClient.subscribe("openhabian/ESP8266/Ref/DPS310/Pressure")


# When the client receives a CONNACK message from the broker in response 
# to the connect it generates an on_connect() callback.

	# starts a background thread to handle the network traffic 
	# and will return immediately
	myClient.loop_start()
	time.sleep(5)
	myClient.loop_stop()
	return offset_Calculation()

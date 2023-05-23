# Date:         19.02.2020 (last update)
# Author:       Miriam Nold
# Project:      Demoanwendung des Sturzerkennungssystems
# Description:  In this code an MQTT publisher is generated when a
#		threshold value in height difference is recognized

import MySQLdb
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
import time


#Open database connection:
myDB = MySQLdb.connect("localhost","user","password","ESP_Data")  #"host","user","password","database"
myCursor = myDB.cursor()

# Called when the broker responds to our connection request.
def on_connect(client, userdata, flags, rc):
	print("Connectes with result code" + str(rc))

def start():

	# Create a client instance with the name myClient
	myClient = mqtt.Client()
	myClient.on_connect = on_connect
	myClient.connect("localhost")
#	myClient.loop_start()

	while(True):
		myDB.commit()
		ti = (datetime.now()- timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
		t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		sql = "SELECT AVG(deltaHigh_with_Offset) FROM SensorData WHERE Time = '" + ti + "' GROUP BY Time;"
	#	print(sql)
		myCursor.execute(sql)
		temp = myCursor.fetchone()
		print temp[0]
	 	if temp[0] < (-200):
			print ("red")
			myClient.publish("openhabian/alert", "red", qos=1)
#		time.sleep(0.5)

	# disconnect from server
	myDB.close()

start()

# Date: 	19.02.2020 (last update)
# Author:	Miriam Nold
# Project: 	Demoanwendung des Sturzerkennungssystems
# Description:  This program is the main script for the data processing.
#		        It calls the skript for the Offset calculation and for the
#		        script to save the data in the Databank

import calculateOffset	# this codes you find in the same folder as the main code
import saveInDatabase

print("Sie sind im Hauptprogramm")
print("Der Offset wird 10s lang berechnet")
offset = calculateOffset.start()
print ("der Offset wurde mit einem wert von " + str(offset) + " berechnet.")

print("Die daten werden nun in die Datenbank eingelesen ")
saveInDatabase.start(offset)

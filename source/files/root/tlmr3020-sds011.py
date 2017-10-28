#!/tmp/usr/bin/python
# -*- coding: utf-8 -*-

# Script to control the air quality sensor SDS011 on a flashed TL-MR3020
# by Maarten Reyniers, based on the scripts of Frank Heuer.
# Documentation on https://github.com/mrtnrey/sds011

import time
import sys
import json
import os
from sds011 import SDS011

serialNumber = "TEST"

if os.path.isfile('./tlmr3020sn.txt'):
	with open("./tlmr3020sn.txt", "r") as infile:
		serialNumber = infile.read().strip()

if serialNumber == "TEST":
	print("Sensor is running in TEST mode and will not report values to madavi.de or")
	print("luftdaten.info. To start reporting to these servers, provide the serial number of")
	print("your TL-MR3020 (13 digits) in the file \"tlmr3020sn.txt\" and restart the script.")

# First create the sensor instance.
# On a TL-MR3020, the sensor is mounted on /dev/ttyUSB0
# Note that this can be different on other devices.
sensor = SDS011('/dev/ttyUSB0', timeout=2, unit_of_measure=SDS011.UnitsOfMeasure.MassConcentrationEuropean)

# Set the dutycycle to two minutes (luftdaten standard)
sensor.dutycycle = 2

# Print some info on the device and the sensor
print("TLMR-3020 S/N read from tlmr3020sn.txt: %s" % serialNumber)
print("SDS011 device ID: %s" % sensor.device_id)
print("SDS011 device firmware: %s" % sensor.firmware)

# Create a json string with this info, and store this string in a text file for the dashboard
jsondict=dict([('tlmr3020sn',str(serialNumber)),('SDS011_deviceid', sensor.device_id), ('SDS011_firmware',sensor.firmware)])
jsonstr=json.dumps(jsondict)
with open("/www/sensorNode.json", "w") as outfile:
	outfile.write("%s" % jsonstr)

# Prepare (part of) the header that will be sent to madavi.de and luftdaten.info
if serialNumber != "TEST":
	sensorHeader='X-Sensor: tlmr3020-' + serialNumber

try:
	while True:

		values = sensor.get_values()

		if values is not None:

			print("PM2.5  ", values[1], ", PM10 ", values[0])

			# Put the values in a json string for the dashboard and the APIs
			pm10=dict([('value_type', 'SDS_P1'), ('value', str(values[0]))])
			pm25=dict([('value_type', 'SDS_P2'), ('value', str(values[1]))])
			jsondict=dict([('software_version', 'github.com/mrtnrey/sds011'), ('sensordatavalues',[pm25,pm10])])
			jsonstr=json.dumps(jsondict)

			# Store the json string with the values and the time of measurement in text files for dashboard
			with open("/www/SDS011LatestValues.json", "w") as outfile:
				outfile.write("%s" % jsonstr)
			with open("/www/SDS011LatestTime.txt", "w") as outfile:
				outfile.write("%s" % str(int(time.time())))

			# Here you can add a curl command to send the data to a local server in your LAN (e.g. Raspberry Pi)
			# that stores the measurements in a local database
			### curlcmd='curl -s -H "' + header + '" -d "' + jsonstr + '" http://rpi/receive.php'

			# If serialNumber is set, then send data to madavi.de and luftdaten.info
			if serialNumber != "TEST":

				# SEND TO MADAVI.DE
				curlcmd='/tmp/usr/bin/curl -s -H "Content-Type: application/json" -H "X-Pin: 1" -H "' + sensorHeader + '" -d \'' + jsonstr + '\' https://api-rrd.madavi.de/data.php'
				status = os.popen(curlcmd).readlines()
				# Store time and response in text files for the dashboard 
				with open("/www/madaviLatestTime.txt", "w") as outfile:
					outfile.write("%s" % str(int(time.time())))
				with open("/www/madaviLatestResponse.txt", "w") as outfile:
					outfile.write("%s" % str(status))

				# SEND TO LUFTDATEN.INFO
				curlcmd='/tmp/usr/bin/curl -s -H "Content-Type: application/json" -H "X-Pin: 1" -H "' + sensorHeader + '" -d \'' + jsonstr.replace("SDS_", "") + '\' https://api.luftdaten.info/v1/push-sensor-data/'
				status = os.popen(curlcmd).readlines()
				# Store time and response in text files for the dashboard 
				with open("/www/luftdatenLatestTime.txt", "w") as outfile:
					outfile.write("%s" % str(int(time.time())))
				with open("/www/luftdatenLatestResponse.txt", "w") as outfile:
 					outfile.write("%s" % str(status))

		time.sleep(10) # check every ten seconds for new values

except:
	sensor.reset()
	sensor = None
	sys.exit("Sensor has been reset")

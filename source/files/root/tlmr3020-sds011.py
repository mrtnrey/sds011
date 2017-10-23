#!/tmp/usr/bin/python
# -*- coding: utf-8 -*-

import time
import sys
import json
import os
from sds011 import SDS011

serialNumber = "TEST"

if os.path.isfile('./tlmr3020sn.txt'):
	f = open("./tlmr3020sn.txt", "r")
	serialNumber = f.read().strip()
	f.close()

if serialNumber == "TEST":
	print("Sensor is running in test mode and will not report values to madavi.de.")
	print("To start reporting to madavi.de, provide the serial number of your")
	print("TL-MR3020 in the file \"tlmr3020sn.txt\" and restart the script.")

sensor = SDS011('/dev/ttyUSB0', timeout=2, unit_of_measure=SDS011.UnitsOfMeasure.MassConcentrationEuropean)

sensor.dutycycle = 2

print("TLMR-3020 S/N read from tlmr3020sn.txt: %s" % serialNumber)
print("SDS011 device ID: %s" % sensor.device_id)
print("SDS011 device firmware: %s" % sensor.firmware)

jsondict=dict([('tlmr3020sn',str(serialNumber)),('SDS011_deviceid', sensor.device_id), ('SDS011_firmware',sensor.firmware)])
jsonstr=json.dumps(jsondict)
f = open("/www/sensorNode.json", "w")
f.write("%s" % jsonstr)
f.close()

sensorHeader='X-Sensor: tlmr3020-' + serialNumber

try:
	while True:
		values = sensor.get_values()
		if values is not None:
			print("PM2.5  ", values[1], ", PM10 ", values[0])
			pm10=dict([('value_type', 'SDS_P1'), ('value', str(values[0]))]) # luftdaten requires value as string
			pm25=dict([('value_type', 'SDS_P2'), ('value', str(values[1]))])
			sensorarr=[pm25,pm10]
			jsondict=dict([('software_version', 'github.com/mrtnrey/sds011'), ('sensordatavalues',sensorarr)])
			jsonstr=json.dumps(jsondict)
			f = open("/www/SDS011LatestValues.json", "w")
			f.write("%s" % jsonstr)
			f.close()
			f = open("/www/SDS011LatestTime.txt", "w")
			f.write("%s" % str(int(time.time())))
			f.close()

			# Send to my RPi
			# curlcmd='curl -s -H "' + header + '" -d "' + jsonstr + '" http://rpi/receive.php'

			# Send to madavi.de if serialNumber is set
			if serialNumber != "TEST":
				curlcmd='/tmp/usr/bin/curl -s -H "Content-Type: application/json" -H "X-Pin: 1" -H "' + sensorHeader + '" -d \'' + jsonstr + '\' https://api-rrd.madavi.de/data.php'
				print("%s" % curlcmd)
				status = os.popen(curlcmd).readlines()
				print(status)
				f = open("/www/madaviLatestTime.txt", "w")
				f.write("%s" % str(int(time.time())))
				f.close()
				f = open("/www/madaviLatestResponse.txt", "w")
				f.write("%s" % str(status))
				f.close()
		time.sleep(10)
except:
	sensor.reset()
	sensor = None
	sys.exit("Sensor has been reset")

# Fine dust sensor SDS011 on a flashed router
Reading a SDS011 sensor on a flashed TP-Link TL-MR3020 running LEDE + Python, and send your measurement to madavi.de (option) over a **wired connection**.

![SDS011 dashboard screenshot](https://github.com/mrtnrey/sds011/blob/master/imgs/tlmr3020+SDS011.jpg)
*A perfect marriage: an SDS011 (left) connected to a flashed TL-MR3020*

## CAUTION
Although the software is tested & running on my own device, you should be aware of flashing a router is not without risk.
At least some basic knowledge of linux is required.
If you flash your router,
- warranty is lost
- firmware of manufacturer is lost
- bricking your router is not completely excluded.

Concerning latter point: the TL-MR3020 router can be unbricked quite easily (own experience...).

## Motivation
If you have access to a Wifi network (e.g. your own), don't read further and order an ESP8266, follow the instructions on [Luftdaten.info](http://luftdaten.info), and you're set.
If
- you don't have access to Wifi, only to a wired network,
- or you would like to have more control on your SDS011 with Python

then you can consider this repository.

## How to install
For installing the software, you have two possibilities
#### Method 1: flash with LEDE images
Flash your TL-MR3020 with a LEDE image containing everything you need.
Further instructions in the readme of /baked_firmware.
#### Method 2: build it yourself
Build it yourself with the instructions and sources provided.
This procedure should also hold for routers other than the TL-MR3020.
Further instructions in the readme of /source.

## After installation
The TL-MR3020 expects the SDS011 already connected the USB port while booting.
In the /root directory you'll find the file tlmr3020sn.txt, containing "TEST".
If you would like your device sending data to Madavi, you have to replace the word "TEST" with the serial number of your TL-MR3020. This has to be done manually since the TL-MR3020 is ignorant on its own serial number.

## Dashboard on local webpage
Inside your LAN you will have a basic webpage [http://tlmr3020](http://tlmr3020/)
informing you on the latest measurements.
It is on purpose very light, to keep the load low. The S/N of my device is blurred.

![SDS011 dashboard screenshot](https://github.com/mrtnrey/sds011/blob/master/imgs/SDS011dashbrd.jpg)
*SDS011 local dashboard screenshot*


## TO DO
- Beautify & comment the Python script
- Running the script as a service that you can start() and stop().
- Exception handling
- Monitor the memory usage of the router to avoid memory starvation
- ...

## Acknowledgements
- Frank Heuer for [his python script](https://gitlab.com/frankrich/sds011_particle_sensor) that is used here
- the [OpenWRT](https://www.openwrt.org) / [LEDE](https://lede-project.org) project
- the [Luftdaten](http://luftdaten.info) guys


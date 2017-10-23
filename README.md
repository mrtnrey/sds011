# Fine dust sensor SDS011 on a flashed router
Reading a SDS011 sensor on a flashed TP-Link TL-MR3020 running LEDE + Python, and send your measurement to madavi.de (option) over a **wired connection**.


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
### Method 1: flash with LEDE images
Flash your TL-MR3020 with a LEDE image containing everything you need.
Further instructions in the readme of /baked_firmware.
### Method 2: build it yourself
Build it yourself with the instructions and sources provided.
This procedure should also hold for routers other than the TL-MR3020.
Further instructions in the readme of /baked_firmware.

## Acknowledgements
- respository of Frank Heuer https://gitlab.com/frankrich/sds011_particle_sensor
- the [OpenWRT](https://www.openwrt.org) / [LEDE](https://lede-project.org) project
- the [Luftdaten](http://luftdaten.info) guys

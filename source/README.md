## Building a LEDE image for your router to control the SDS011 sensor

The steps below guide you through the process of building a firmware for your router that is capabale of controlling your SDS011 sensor and send the data to madavi.de and luftdaten.info. The procedure is tested on a TP-LINK TL-MR3020, but should also work for other routers with USB port.

### 1. Get an linux machine and install the LEDE image builder
Having an machine running a Debian/Ubuntu or a CentOS/RHEL flavour is necessary. If you have a Mac or Windows, create a virtual machine running one of these. I did this on a Mac running VirtualBox which is free Oracle software.
Read the docs on the [LEDE Image Builder](https://lede-project.org/docs/user-guide/imagebuilder) before continuing!

### 2. Copy the files in /files of the repository to the path of the LEDE image builder
(TO DO)

### 3. Get an linux machine and install the LEDE image builder
We will build a custom stripped-down LEDE image since we want to have some free space on the device in order to keep the system smoothly operating. Therefore, we will omit the LuCI components, so you will not be able to control your flashed device by the web UI. This implies some basic knowledge of Linux and Pyhton of your side (but nothing complicated).

Now issue this build command:

```bash
make image PROFILE=tl-mr3020-v1 PACKAGES="-libiwinfo-lua -liblua -libubus-lua -libuci-lua -lua -luci -luci-app-firewall -luci-base -luci-lib-ip -luci-lib-nixio -luci-mod-admin-full -luci-proto-ipv6 -luci-proto-ppp -luci-theme-bootstrap uhttpd kmod-usb-serial-ch341 nano" FILES="files/"
```
Basically, it strips down the default image, but it adds these three packages:
- uhhtpd: the OpenWRT ultralight web server
- kmod-usb-serial-ch341: driver for the UART2USB that comes with your SDS011 sensor
- nano: strictly not needed, but nice to have if you think of Vim being a cleaning product

Of course, _you should replace the PROFILE with the PROFILE appropriate for your router_, if you have a device other than the TL-MR3020 I am using.

After successfully building the image, you can retreive it in bin/target/...
Now follow the instructions given in /prebaked_firmware

## What's in /files ?
It is important to have some basic understanding of how the flashed device is working.

In ```/root```, the main Python scripts are stored, being ... (TO DO)

In  ```/www```, the file ```index.html``` will provide a minimal dashboard for the sensor status.

The most important files, however, are given in ```/etc```
**Since the flash memory of most routers (like the TL-MR3020) is too small to accomodate Python and the necesarry packages, we need to install it in the RAM during boot.**  Every time the device boots, these packges have to be freshly installed.
Luckily, the file ```/etc/rc.local``` takes care of this.

```
opkg update
opkg install python-light -d ram
opkg install python-pyserial -d ram
opkg install python-enum34 -d ram
opkg install python-logging -d ram
opkg install curl -d ram
opkg install ca-bundle -d ram
cd /root && LD_LIBRARY_PATH=/tmp/usr/lib/ ./tlmr3020-sds011.py > /dev/null 2>&1 &
```

Curl and the ca-bundle are needed to upload your data to madavi.de and luftdaten.info. If you intend to run your sensor strictly locally, you can omit these.

The last line starts the SDS011 control script, so it is important to have your SDS011 already connected to your flashed router during boot.

In ```/etc/rc.local/network``` the network connection is defined. The flashed router should be connected to your LAN with an ethernet cable. The flashed router is then requesting an IP address and will request the hostname "tlmr3020". Obviously you can alter this with your prefered settings.

## What if this goes terribly wrong?
Flashing a router is never without risk. If you flash with an incompatible firmware, your router can become irresponsive ("bricked"). You can consider this a part of the learing process :)
Anyway, at least for the TL-MR3020 there are excellent cookbooks you can follow to unbrick your router.
I had the experience myself, and I followed these two guides to successfully unbrick my device:
[http://techjim.blogspot.be/2014/11/how-to-unbrick-tp-link-mr3020-on-osx.html]
[http://blog.khairulazam.net/2015/02/16/recover-bricked-tl-mr3020-via-serial-console/]
One advice is don't give up too quickly.


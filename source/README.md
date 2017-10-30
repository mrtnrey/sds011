## Building a LEDE image for your router to control the SDS011 sensor

The steps below guide you through the process of building a firmware for your router that is capabale of controlling your SDS011 sensor and send the data to madavi.de and luftdaten.info. The procedure is tested on a TP-LINK TL-MR3020, but should also work for other routers with USB port.

### 1. Get an linux machine and install the LEDE image builder
Having an machine running a Debian/Ubuntu or a CentOS/RHEL flavour is necessary. If you have a Mac or Windows, create a virtual machine running one of these. I did this on a Mac running VirtualBox which is free Oracle software.
Read the docs on the [LEDE Image Builder](https://lede-project.org/docs/user-guide/imagebuilder) before continuing!

### 2. Copy the files in /files of the repository to the path of the LEDE image builder

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

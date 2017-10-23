## Prebaked firmware image
The images above can be used to flash your router.

### Attention
the firmware does not come with the gui to control your device after flashing (LuCI).
Although no programming of your side is required, it is important to master some basic linux and python.

### Procedure
The image is a custom build LEDE image, with the necessary files added.

If you are already running OpenWRT or LEDE on your TL-MR3020, you can flash the firmware with the "sysupgrade" command and the image

If you are flashing from the manufacturer's firmware, flash with the Gui and the image

Before flashing, already connect the SDS011 to the USB port of your TL-MR3020 and with an ethernet cable. After flashing, the router will request an IP address via dhcp through the ethernet port.

Flashing takes about one or two minutes. Wait until all LEDs have stopped blinking.

The router now has the hostname "tlmr3020". Check if the webpage "http://tlmr3020/" is accessible in your LAN. If it is not the case, try to find the IP address that was assigned to your device.

On the page http://tlmr3020/" you should see the first measurements after a few minutes. If the line "SDS011 firmware" is not filled out, do a hard reset of your router (power off/on).

import network
import time
import secret
import urequests

import EPD_7in5_B

SSID = secret.SSID
PW = secret.PW
IP_ADDRESS = '192.168.0.161'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PW)

while wlan.isconnected() == False:
    print('Connecting to Wi-Fi router')
    time.sleep(1)

wlan_status = wlan.ifconfig()
#wlan.ifconfig((IP_ADDRESS, wlan_status[1], wlan_status[2], "8.8.8.8"))

wlan_status = wlan.ifconfig()
print('Connected!')
print(f'IP Address: {wlan_status[0]}')
print(f'Netmask: {wlan_status[1]}')
print(f'Default Gateway: {wlan_status[2]}')
print(f'Name Server: {wlan_status[3]}')
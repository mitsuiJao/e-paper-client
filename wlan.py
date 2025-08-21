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

def __urlencode(s):
    encoded_str = ''
    for char in s:
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z' or '0' <= char <= '9' or char in '-_.~':
            encoded_str += char
        else:
            encoded_str += ''.join(['%{:02X}'.format(b) for b in char.encode('utf-8')])
    return encoded_str

def request_API(url, **kwargs):
    requestURL = url
    requestURL += "?"
    for key in kwargs.keys():
        requestURL += key
        requestURL += "="
        requestURL += __urlencode(kwargs[key])
        
    res = urequests.get(requestURL)
    if res.status_code == 200:
        dirdate = res.json()
    else:
        return
    
    res.close()

    return dirdate

"""
bm = get_font("米子高専総合工学科4年 西山")
print(bm)

epd = EPD_7in5_B.EPD_7in5_B()
epd.Clear()
epd.imageblack.fill(0xff)
epd.imagered.fill(0x00)

jpblackchar(epd, bm["bitmap"][0], 10, 10, 5)
epd.display()
"""
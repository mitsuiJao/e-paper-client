from e_paper import epd7in5b_V2
from e_paper import epdconfig
import requests


epd = epd7in5b_V2.EPD()
try:
    size = 480*800 // 8 
    url = "https://mitsuijao.fun/api/weather"
    payload = {}
    headers = {}

    res = requests.request("GET", url, headers=headers, data=payload)

    if res.status_code == 200:
        black = res.content[:size]
        red = res.content[size:]


        epd.init()
        epd.Clear()
        epd.display(bytearray([255 - b for b in black]), bytearray([255 - r for r in red]))
    
    else:
        print("connection error")
        print(res.status_code)
        print(res.text)

except Exception as e:
    print(e)

finally:
    epd.sleep()
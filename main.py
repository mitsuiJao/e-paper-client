import machine
import time
import urequests
import wlan
import ntptime

import EPD_7in5_B
import framebuf2 as framebuf

from drawString import drawString

WEEK = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
WEEKDAY = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

YEAR = 2025
MONTH = 8
DAY = 20

epd = EPD_7in5_B.EPD_7in5_B()
        

def Zeller(y, m, d):
    if m == 1 or m == 2:
        m += 12
        y -= 1
    w = d + int((13 * m + 8) / 5) + y + int(y / 4) - int(y / 100) + int(y / 400)
    h = w % 7
    return h


def create_calendar(y, m):
    DAYS30 = [4, 6, 9, 11]
    h = Zeller(YEAR, MONTH, 1)
    
    if m == 2:
        if (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0):
            maxday = 29
        else:
            maxday = 28
    elif m in DAYS30:
        maxday = 30
    else:
        maxday = 31

    c = []
    day = 1
    for i in range(6):
        tmp = []
        for j in range(7):
            if j < h and i == 0:
                tmp.append(0)
            elif day <= maxday:
                tmp.append(day)
                day += 1
            else:
                tmp.append(0)

        c.append(tmp)

    if not any(c[-1]):
        c.pop()
    if not any(c[-1]):
        c.pop()


    print(c)
    return c

def get_shukujitsu():
    shukujitsu_URL = f"https://holidays-jp.github.io/api/v1/{YEAR}/date.json"
    res = urequests.get(shukujitsu_URL)
    if res.status_code == 200:
        dirdate = res.json()
    else:
        dirdate = {}
    
    res.close()
 
    shukujitsu_date = [[] for _ in range(12)]
    for date in dirdate.keys():
        shukujitsu_date[int(date[5:7])].append(int(date[-2:]))
    
    return shukujitsu_date, dirdate

def get_date():
    NTP = "ntp.nict.jp"
    ntptime.host = NTP
    ntptime.settime()
    return time.localtime(time.time() + (9 * 60 * 60))

def get_events():
    SERVER_URL = "http://192.168.0.102/api/events"
    res = urequests.get(SERVER_URL)
    if res.status_code == 200:
        dirdate = res.json()
    else:
        return
    
    res.close()

    return dirdate

def format_event(s, e):
    result = {}
    sd = s[8:10]
    ed = e[8:10]
    sm = s[5:7]
    em = e[5:7]
    st = ""
    et = ""
    result["sm"] = sm
    result["sd"] = sd
    result["st"] = ""
    result["et"] = ""

    is_allday = True
    if len(s) > 10:
        is_allday = False
        st = s[11:16]
        et = e[11:16]
    else:
        result["st"] = ("All day")
    
    if sd == ed and sm == em and not is_allday:
        result["st"] = st
        result["et"] = et
    elif ((sd != ed) or (sd == ed and sm != em)) and not is_allday:
        result["st"] = st

    return result

def get_font(string):
    SERVER_URL = f"http://192.168.0.102/api/font?q={string}"
    res = urequests.get(SERVER_URL)
    if res.status_code == 200:
        dirdate = res.json()
    else:
        return
    
    res.close()

    return dirdate

shukujitsu_date, shukujitsu = get_shukujitsu()
e = get_events()


epd.Clear()

epd.imageblack.fill(0xff)
epd.imagered.fill(0x00)

epd.imageblack.line(500, 0, 500, 480, 0x00)
epd.imageblack.line(0, 88, 500, 88, 0x00)

drawString(epd, f"{YEAR}", 32, 48, 2)
drawString(epd, f"{MONTH:02}/{DAY:02}", 116, 28, 5, 0x00)
drawString(epd, f"{WEEKDAY[Zeller(YEAR, MONTH, DAY)]}", 336, 28, 5, 0x00)

#epd.imageblack.large_text(f"{YEAR}", 32, 48, 2, 0x00)
#epd.imageblack.large_text(f"{MONTH:02}/{DAY:02}", 116, 28, 5, 0x00)
#epd.imageblack.large_text(f"{WEEKDAY[Zeller(YEAR, MONTH, DAY)]}", 336, 28, 5, 0x00)

y = 120
for index, weekstr in enumerate(WEEK):
    if index == 0:
        drawString(epd, weekstr, 32, y, 3, True)
        #epd.imagered.large_text(weekstr, 32, y, 3, 0xff)
    else:
        drawString(epd, weekstr, 32+(index*64), y, 3)
        #epd.imageblack.large_text(weekstr, 32+(index*64), y, 3, 0x00)
    
c = create_calendar(YEAR, MONTH)

weeklen = len(c)
dy = 56
if weeklen == 6:
    dy = 48
if weeklen == 4:
    dy = 64
    
y += dy
for i in c:
    x = 32
    for index, day in enumerate(i):
        if day == 0:
            pass
        else:
            if day == DAY:
                fill = True
            else:
                fill = False
                
            if index == 0 or day in shukujitsu_date[MONTH]:
                red = True
            else:
                red = False
                
            drawString(epd, f"{day:>2}", x, y, 3, red, fill, 4, 8)

        x += 64
    y += dy
    
x = 524
events = e.get("events")
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    formatted = format_event(start, end)
    drawString(epd, formatted["sm"], 524, 32, 2)
    drawString(epd, formatted["sd"], 576, 40, 4)
    drawString(epd, formatted["st"], 624, 48, 3)
    drawString(epd, u"ペットボトルの日", 524, 80, 4)
    
    


epd.display()
 

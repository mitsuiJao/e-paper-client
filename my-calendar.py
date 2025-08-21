import calendar
import datetime
import EPD_7in5_B
import framebuf2 as framebuf

epd = EPD_7in5_B.EPD_7in5_B()

epd.Clear()

epd.imageblack.fill(0xff)
epd.imagered.fill(0x00)


now = datetime.datetime.now()
y = now.year
m = now.month
calendar_now = calendar.monthcalendar(y, m)

epd.imageblack.large_text("this is framebuf2 liblary method!", 5, 30, 2, 0x00)
epd.display()


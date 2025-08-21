import EPD_7in5_B
from drawString import drawString

epd = EPD_7in5_B.EPD_7in5_B()
epd.Clear()
epd.imageblack.fill(0xff)
epd.imagered.fill(0x00)

string = "米子高専総合工学科4年西山"
drawString(epd, string, 10, 10, 4)

epd.display()

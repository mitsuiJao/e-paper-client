import wlan
import urequests

class drawString():
    def __init__(self, EPD_instance, string, x, y, size=1, is_red=False, is_filled=False, dx=0, dy=0, align="l", lenght=0):
        self.string = string
        self.size = size
        self.is_red = is_red
        self.is_filled = is_filled
        self.dx = dx
        self.dy = dy
        self.align = align
        self.lenght = lenght
        self.epd = EPD_instance
        
        self.x, self.y = self.point(x, y)
        
        if len(string) == len(string.encode("utf-8")):
            self.is_japanese = False
        else:
            self.is_japanese = True
        
        if self.is_filled:
            self.fill()
        
        if self.is_japanese:
            self.jadraw()
        else:
            self.draw()

    def draw(self):
        if self.is_red:
            self.epd.imagered.large_text(self.string, self.x, self.y, self.size, 0xff)
        elif not self.is_filled:
            self.epd.imageblack.large_text(self.string, self.x, self.y, self.size, 0x00)
        else:
            self.epd.imageblack.large_text(self.string, self.x, self.y, self.size, 0xff)
            self.epd.imagered.large_text(self.string, self.x, self.y, self.size, 0x00)

    def fill(self):
        if self.is_red:
            self.epd.imagered.fill_rect(self.x-self.dx, self.y-self.dy, (8*len(self.string)*self.size)+(self.dx*2), 8*self.size+self.dy*2, 0xff)
        else:
            self.epd.imageblack.fill_rect(self.x-self.dx, self.y-self.dy, (8*len(self.string)*self.size)+(self.dx*2), 8*self.size+self.dy*2, 0x00)
            
    def point(self, x, y):
        if self.align == "l":
            return x, y
        elif self.align == "c":
            offset_char = int((self.lenght - len(self.string)) / 2)
            offset_px = offset_char * 8 * self.size
            return offset_px, self.y
        elif self.align == "r":
            offset_char = self.lenght - len(self.string)
            offset_px = offset_char * 8 * self.size
            return offset_px, self.y
        
    def _jpchar(self, epd, fd, x, y, scale):
        for row in range(0, 7):
            for col in range(0, 7):
                if (0x80 >> col) & fd[row]:
                    for dy in range(scale):
                        for dx in range(scale):
                            if self.is_red:
                                epd.imagered.pixel(col * scale + x + dx, row * scale + y + dy, 0xff)                
                            elif not self.is_filled:
                                epd.imageblack.pixel(col * scale + x + dx, row * scale + y + dy, 0x00)                
                            else:
                                epd.imageblack.pixel(col * scale + x + dx, row * scale + y + dy, 0xff)
                                epd.imagered.pixel(col * scale + x + dx, row * scale + y + dy, 0x00)
                            
    def _char(self, epd, c, x, y, scale):
        if self.is_red:
            self.epd.imagered.large_text(c, x, y, self.size, 0xff)
        elif not self.is_filled:
            self.epd.imageblack.large_text(c, x, y, self.size, 0x00)
        else:
            self.epd.imageblack.large_text(c, x, y, self.size, 0xff)
            self.epd.imagered.large_text(c, x, y, self.size, 0x00)

              
    def jadraw(self):
        x = self.x
        for c in self.string:
            if len(c) == len(c.encode("utf-8")):
                self._char(self.epd, c, x, self.y, self.size)
                
            else:
                bm = wlan.request_API("https://192.168.0.102/api/font", q=c)
                self._jpchar(self.epd, bm["bitmap"], x, self.y, self.size)
            
            x += 8*self.size

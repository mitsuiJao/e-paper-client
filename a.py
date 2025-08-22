import urequests
import gc
import wlan
import EPD_7in5_B

# EPDの初期化
epd = EPD_7in5_B.EPD_7in5_B()

BUFFER_SIZE = 800 * 480 // 8
COMBINED_SIZE = BUFFER_SIZE * 2

def get_epaper_data_stream(url):
    # リクエストを送信する前に、ガベージコレクションを実行してメモリを整理
    gc.collect()

    # urequestsがメモリを確保できるように、既存のバッファを一時的に解放
    # epd.buffer_black = None
    # epd.buffer_red = None
    
    res = urequests.get(url, stream=True)

    if res.status_code == 200:
        epd.buffer_black = bytearray(BUFFER_SIZE)
        epd.buffer_red = bytearray(BUFFER_SIZE)
        gc.collect()

        offset = 0

        while offset < COMBINED_SIZE:
            chunk_size = 4096
            chunk = res.raw.read(chunk_size)
            if not chunk:
                break
            
            if offset < BUFFER_SIZE:
                epd.buffer_black[offset : offset + len(chunk)] = chunk
            else:
                epd.buffer_red[offset - BUFFER_SIZE : offset - BUFFER_SIZE + len(chunk)] = chunk
            
            offset += len(chunk)
            gc.collect()
        
        res.close()

        
URL = "http://192.168.0.102/api/calendar"

# epd.buffer_blackとepd.buffer_redをEPD_7in5_Bクラスの初期化から削除する必要がある
get_epaper_data_stream(URL)
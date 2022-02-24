# nohup python3 stats.py &

import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import socket
import json


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 270

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 22)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

pagenum=1

sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sck.bind(('127.0.0.1', 5555))
sck.setblocking(0)

msg = "Listening..."
y = font.getsize(msg)[1]*2
draw.text((x, y), msg, font=font, fill="#FFFF00")
disp.image(image, rotation)

lastCallsign = ""
curCallsign = ""
rowSpacing = 3

while True:

    try:
        data, address = sck.recvfrom(1024)

    except Exception as msg:
        pass

    else:
        rawData = data.decode('utf-8').replace("\r\n","");
        print(rawData)
        try:
            j = json.loads(rawData)

        except Exception as xcp:
            print(str(xcp))
            print(data)
            
        curCallsign = j['flight']
        timestamp = time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(j['timestamp']))
        msgno = j['msgno']
        if 'text' in j:
            hasText = True
            s_message = j['text']
            s_width = 20
            s_padding = ''.ljust(s_width - 1)
            s_text = s_padding + s_message + s_padding
            s_idx = 0

        else:
            hasText = False
            
    finally:
        if (curCallsign != lastCallsign):
            lastCallsign = curCallsign

            draw.rectangle((0, 0, width, height), outline=0, fill=0)

            y = top

            cs_msgno = curCallsign + " " + msgno
            draw.text((x, y), cs_msgno, font=font, fill="#FFFFFF")
            y += font.getsize(cs_msgno)[1] + rowSpacing

            draw.text((x, y), timestamp, font=font, fill="#FFFF00")
            y += font.getsize(timestamp)[1] + rowSpacing

            if hasText:
                draw.text((x, y), s_message[0:20], font=font, fill="#FF00FF")

            disp.image(image, rotation)
        
        #if buttonA.value:
        #    draw.rectangle((0, 0, width, height), outline=0, fill=0)
        #    draw.text((x, 40), "Shutdown", font=font, fill="#FF0000")
        #    disp.image(image, rotation)

        # scroll existing test




#    s_message = "This is a test of a very long scrolling message with no CR or LFs."
#    s_width = 20
#    s_padding = ''.ljust(s_width - 1)
#    s_text = s_padding + s_message + s_padding
#    for idx in range(0, len(s_text) - s_width + 1):
#        callsign="US1735"
#        logdatetime="11-23-21 20:08:46"
#        msgNum=f'({pagenum}) N354'
#        y = top
#        draw.text((x, y), callsign, font=font, fill="#FFFFFF")
#        y += font.getsize(callsign)[1] + 2
#        draw.text((x, y), logdatetime, font=font, fill="#FFFF00")
#        y += font.getsize(logdatetime)[1] + 2
#        draw.text((x, y), msgNum, font=font, fill="#0000FF")
#        y += font.getsize(msgNum)[1] + 2
#        
#        draw.text((x, y), s_text[idx:idx+s_width], font=font, fill="#FF00FF")
#        disp.image(image, rotation)
#        time.sleep(0.05)
#        draw.rectangle((0, 0, width, height), outline=0, fill=0)
#
#        if buttonA.value:
#            pagenum = pagenum - 1
#            if pagenum < 0:
#                pagenum = 1
#
#        if buttonB.value:
#            pagenum += 1
#
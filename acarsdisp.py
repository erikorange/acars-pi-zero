# nohup python3 stats.py &

import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import socket
import json
from subprocess import call


def getData():
    try:
        data, address = sck.recvfrom(1024)

    except Exception as msg:
        return(False, "")

    else:
        rawData = data.decode('utf-8').replace("\r","").replace("\n","");
        try:
            j = json.loads(rawData)

        except Exception as xcp:
            return(False, "")

        else:
            return(True, j)


def paintInfo(packet, draw, width, height, x, top, csFont, font, msgFont, idx, numPackets, disp, image, rotation):
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    y = top
    # center and draw callsign
    csWidth, csHeight = draw.textsize(packet['flight'], font=csFont)
    draw.text((x + (width - csWidth)/2, y), packet['flight'], font=csFont, fill=(0, 255, 0))
    
    # draw timestamp
    draw.text((x, 40), packet['timestamp'], font=font, fill="#FFFF00")
    
    # draw message
    mWidth, mHeight = draw.textsize(packet['message'], font=msgFont)
    if (mWidth > width):
        x_msg = width       # scrollable, draw offscreen
    else:
        x_msg = 0           # not scrollable, draw onscreen
    draw.text((x_msg, 70), packet['message'], font=msgFont, fill="#FF00FF")

    # center and draw the count
    countStr = f'{idx} of {numPackets}'
    cWidth, cHeight = draw.textsize(countStr, font=font)
    draw.text((x + (width - cWidth)/2, 105), countStr, font=font, fill=(0, 255, 255))

    # repaint screen
    disp.image(image, rotation)
    return(mWidth, mHeight, x_msg)



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

# Draw a filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)

top = -5
x = 0
count = 0

font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 22)
msgFont = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 30)
csFont = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 40)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sck.bind(('127.0.0.1', 5555))
sck.setblocking(0)

packets=[]

draw.text((x, 50), "Waiting for ACARS...", font=font, fill="#00FF00")
disp.image(image, rotation)

mWidth = 0
idx = 0
pageNum = 0

while True:
    (status, j) = getData()
    
    if (status):
        if 'text' in j:

        # got an acars packet with a message, extract data
            idx += 1
            pageNum = idx

            p={}
            p['timestamp'] = time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(j['timestamp']))
            p['tail'] = j['tail']
            p['flight'] = j['flight']
            p['message'] = j['text']

            packets.append(p)

            (mWidth, mHeight, x_msg) = paintInfo(packets[idx-1], draw, width, height, x, top, csFont, font, msgFont, idx, len(packets), disp, image, rotation)

        
    

    # update scroll if it's scrollable
    if (mWidth > width):
        draw.rectangle((0, 70, width, 70+mHeight), outline=0, fill=(0, 0, 0))
        x_msg -= 12
        draw.text((x_msg, 70), packets[pageNum-1]['message'], font=msgFont, fill="#FF00FF")
        disp.image(image, rotation)
        if (abs(x_msg) > mWidth):
            x_msg = width

    if not buttonA.value:
        if (idx > 0 and (pageNum > 1)):
            pageNum -= 1
            (mWidth, mHeight, x_msg) = paintInfo(packets[pageNum-1], draw, width, height, x, top, csFont, font, msgFont, pageNum, len(packets), disp, image, rotation)
    
    if not buttonB.value:
        if (pageNum < len(packets)):
            pageNum += 1
            (mWidth, mHeight, x_msg) = paintInfo(packets[pageNum-1], draw, width, height, x, top, csFont, font, msgFont, pageNum, len(packets), disp, image, rotation)
    
    if not buttonA.value and not buttonB.value:
        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        draw.text((0, 50), "SHUTDOWN", font=csFont, fill="#FF0000")
        disp.image(image, rotation)
        call("sudo shutdown now --poweroff", shell=True)
        
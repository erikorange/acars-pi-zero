# nohup python3 stats.py &
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# -*- coding: utf-8 -*-

import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789


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


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono.ttf", 28)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

pagenum=1

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    #cmd = "hostname -I | cut -d' ' -f1"
    #IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
    #cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    #CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB%.2f%%\", $3,$2,$3*100/$2 }'"
    #MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    #Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
    #Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

    s_message = "This is a test of a very long scrolling message with no CR or LFs."
    s_width = 20
    s_padding = ''.ljust(s_width - 1)
    s_text = s_padding + s_message + s_padding
    for idx in range(0, len(s_text) - s_width + 1):
        callsign="US1735"
        logdatetime="11-23-21 20:08:46"
        msgNum=f'({pagenum}) N354'
        y = top
        draw.text((x, y), callsign, font=font, fill="#FFFFFF")
        y += font.getsize(callsign)[1] + 2
        draw.text((x, y), logdatetime, font=font, fill="#FFFF00")
        y += font.getsize(logdatetime)[1] + 2
        draw.text((x, y), msgNum, font=font, fill="#0000FF")
        y += font.getsize(msgNum)[1] + 2
        
        draw.text((x, y), s_text[idx:idx+s_width], font=font, fill="#FF00FF")
        disp.image(image, rotation)
        time.sleep(0.05)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        if buttonA.value:
            pagenum = pagenum - 1
            if pagenum < 0:
                pagenum = 1

        if buttonB.value:
            pagenum += 1



    # Write four lines of text.
    

    # Display image.
    #disp.image(image, rotation)
    #time.sleep(0.1)


# nohup python3 stats.py &

import time
import datetime
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import socket
import json
from subprocess import call

class Display():

    def __init__(self):
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = None
        BAUDRATE = 64000000

        spi = board.SPI()
        self.__disp = st7789.ST7789(
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

        self.__height = self.__disp.width  # we swap height/width to rotate it to landscape!
        self.__width = self.__disp.height
        self.__image = Image.new("RGB", (self.__width, self.__height))
        self.__draw = ImageDraw.Draw(self.__image)
        self.__rotation = 270
        self.__top = -5
        self.__x = 0
        self.__mWidth = 0

        self.__initFonts()
        self.__initColors()
        self.__enableBacklight()
        self.__enableButtons()


    def __initFonts(self):
        self.__font = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 22)
        self.__msgFont = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 30)
        self.__csFont = ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf", 40)

    def __initColors(self):
        self.__black        = (0,0,0)
        self.__green        = (0,255,0)
        self.__yellow       = (255,255,0)
        self.__magenta      = (255, 0, 255)
        self.__red          = (255, 0, 0)
        self.__cyan         = (0, 255, 255)

    def __enableBacklight(self):
        backlight = digitalio.DigitalInOut(board.D22)
        backlight.switch_to_output()
        backlight.value = True

    def __enableButtons(self):
        self.__buttonA = digitalio.DigitalInOut(board.D23)
        self.__buttonB = digitalio.DigitalInOut(board.D24)
        self.__buttonA.switch_to_input()
        self.__buttonB.switch_to_input()
    
    def buttonAPressed(self):
        return(not self.__buttonA.value)

    def buttonBPressed(self):
        return(not self.__buttonB.value)

    def __renderDisplay(self):
        self.__disp.image(self.__image, self.__rotation)

    def clearDisplay(self):
        self.__draw.rectangle((0, 0, self.__width, self.__height), outline=0, fill=self.__black)

    def showOpeningMessage(self):
        self.__draw.text((self.__x, 50), "Waiting for ACARS...", font=self.__font, fill=self.__green)
        self.__renderDisplay()

    def paintInfo(self, packet, idx, numPackets):
        self.clearDisplay()
        y = self.__top

        # center and draw callsign
        csWidth, csHeight = self.__draw.textsize(packet['flight'], font=self.__csFont)
        self.__draw.text((self.__x + (self.__width - csWidth)/2, y), packet['flight'], font=self.__csFont, fill=self.__green)

        # draw timestamp
        self.__draw.text((self.__x, 40), packet['timestamp'], font=self.__font, fill=self.__yellow)

        # draw message
        self.__mWidth, self.__mHeight = self.__draw.textsize(packet['message'], font=self.__msgFont)
        if (self.__mWidth > self.__width):
            self.__x_msg = self.__width       # scrollable, draw offscreen
        else:
            self.__x_msg = 0           # not scrollable, draw onscreen

        self.__draw.text((self.__x_msg, 70), packet['message'], font=self.__msgFont, fill=self.__magenta)

        # center and draw the count
        countStr = f'{idx} of {numPackets}'
        cWidth, cHeight = self.__draw.textsize(countStr, font=self.__font)
        self.__draw.text((self.__x + (self.__width - cWidth)/2, 105), countStr, font=self.__font, fill=self.__cyan)

        self.__renderDisplay()

    def scrollMessage(self):
        if (self.__mWidth > self.__width):
            self.__draw.rectangle((0, 70, self.__width, 70+self.__mHeight), outline=0, fill=self.__black)
            self.__x_msg -= 12
            self.__draw.text((self.__x_msg, 70), packets[pageNum-1]['message'], font=self.__msgFont, fill=self.__magenta)
            self.__renderDisplay()
            if (abs(self.__x_msg) > self.__mWidth):
                self.__x_msg = self.__width

    def flipFlightTail(self, packet, tailFlag):
        if (tailFlag):
            key = 'tail'
        else:
            key = 'flight'

        strWidth, strHeight = self.__draw.textsize(packet[key], font=self.__csFont)
        self.__draw.rectangle((0, 0, self.__width, strHeight), outline=0, fill=self.__black)
        y = self.__top
        self.__draw.text((self.__x + (self.__width - strWidth)/2, y), packet[key], font=self.__csFont, fill=self.__green)
        self.__renderDisplay()
        return
    
    def showShutdownMessage(self):
        self.clearDisplay()
        self.__draw.text((0, 50), "SHUTDOWN", font=self.__csFont, fill=self.__red)
        self.__renderDisplay()


class NetListener():

    def __init__(self, addr, port):
        self.__sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sck.bind((addr, port))
        self.__sck.setblocking(0)
        
    def getData(self):
        try:
            data, address = self.__sck.recvfrom(1024)

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


def loadAcarsData(j):
    p={}
    p['timestamp'] = time.strftime('%m-%d-%Y %H:%M:%S', time.localtime(j['timestamp']))
    p['tail'] = j['tail']
    p['flight'] = j['flight']
    p['message'] = j['text']
    return(p)


display = Display()
display.clearDisplay()
display.showOpeningMessage()

listener = NetListener('127.0.0.1', 5555)

packets=[]
idx = 0
pageNum = 0

startAgain = True
tailFlag = False

while True:
    (status, j) = listener.getData()
    
    if (status):            # got an acars packet
        if 'text' in j:     # with a message
            idx += 1
            pageNum = idx
            packets.append(loadAcarsData(j))
            display.paintInfo(packets[idx-1], idx, len(packets))

    display.scrollMessage()

    if (idx > 0):
        if (startAgain):
            startTime = datetime.datetime.now()
            startAgain = False
        
        endTime = datetime.datetime.now()
        delta = (endTime - startTime).total_seconds()
        if (delta >= 2.0):
            tailFlag = not tailFlag
            startAgain = True
            display.flipFlightTail(packets[pageNum-1], tailFlag)
        

    if display.buttonAPressed():
        if (idx > 0 and (pageNum > 1)):
            pageNum -= 1
            display.paintInfo(packets[pageNum-1], pageNum, len(packets))
    
    if display.buttonBPressed():
        if (pageNum < len(packets)):
            pageNum += 1
            display.paintInfo(packets[pageNum-1], pageNum, len(packets))
    
    if display.buttonAPressed() and display.buttonBPressed():
        display.showShutdownMessage()
        call("sudo shutdown now --poweroff", shell=True)
        
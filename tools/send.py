import socket
import datetime
import time

def loadTestData():
    x=[]
    x.append('{"timestamp":1637698093.4839849,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-14,"error":0,"mode":"2","label":"Q0","block_id":"6","ack":false,"tail":"N641AE","flight":"UA1001","msgno":"M32A","text":"Message1Message1Message1Message1Message1"}')
    x.append('{"timestamp":1637698379.6292551,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-13,"error":0,"mode":"2","label":"5Z","block_id":"4","ack":false,"tail":"N425UA","flight":"UA1002","msgno":"M44A","text":"Message2Message2Message2Message2Message2"}')
    x.append('{"timestamp":1637698389.45926,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-13,"error":0,"mode":"2","label":"5Z","block_id":"5","ack":"S","tail":"N425UA","flight":"UA1003","msgno":"M45A","text":"Message3Message3Message3Message3Message3"}')
    x.append('{"timestamp":1637698403.4676731,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-13,"error":0,"mode":"2","label":"5Z","block_id":"5","ack":false,"tail":"N425UA","flight":"UA1004","msgno":"M45A","text":"Message4Message4Message4Message4Message4"}')
    x.append('{"timestamp":1637698406.9086061,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-13,"error":0,"mode":"2","label":"_d","block_id":"6","ack":"T","tail":"N425UA","flight":"UA1005","msgno":"M45A","text":"Message5Message5Message5Message5Message5"}')
    x.append('{"timestamp":1637698412.561126,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-13,"error":0,"mode":"2","label":"_d","block_id":"7","ack":"U","tail":"N425UA","flight":"UA1006","msgno":"M45A","text":"Message6Message6Message6Message6Message6"}')
    x.append('{"timestamp":1637699948.3995171,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-14,"error":0,"mode":"2","label":"H1","block_id":"6","ack":false,"tail":"N833UA","flight":"UA10013","msgno":"D52A","text":"#DFBA02/A31902,1,1/CCN833UA,NOV23,203256,KLGA,KDEN,2375/C106,06938,5000,96,0010,0,0100,96,X/CEN304,36006,259,781,1397,294,I73014/CNN303,36004,259,781,1396,294/EC011215,01215,00615,73,12,12/EE010690,01215,00615,","end":true}')

    return x


sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sck.connect(('127.0.0.1', 5555))

data = loadTestData()

idx = 1
for dataRec in data:
    msg = bytes(dataRec, 'utf-8')
    retry = True
    while (retry):
        try:
            print(f'Sending {idx} of {len(data)}')
            sck.send(msg)
        except ConnectionRefusedError:
            time.sleep(1)
        except:
            time.sleep(1)
        else:
            retry = False
            idx+=1
    time.sleep(1)

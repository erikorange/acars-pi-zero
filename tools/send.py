import socket
import datetime
import time

def loadTestData():
    x=[]
    x.append('{"timestamp":1637698093.4839849,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-14,"error":0,"mode":"2","label":"Q0","block_id":"6","ack":false,"tail":"N641AE","flight":"PT6176","msgno":"M32A"}')
    x.append('{"timestamp":1637698379.6292551,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-13,"error":0,"mode":"2","label":"5Z","block_id":"4","ack":false,"tail":"N425UA","flight":"UA1003","msgno":"M44A","text":"/B6 DFWEWR EWR R4R"}')
    x.append('{"timestamp":1637698389.45926,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-13,"error":0,"mode":"2","label":"5Z","block_id":"5","ack":"S","tail":"N425UA","flight":"UA1003","msgno":"M45A","text":"/B6 DFWEWR EWR R29"}')
    x.append('{"timestamp":1637698403.4676731,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-13,"error":0,"mode":"2","label":"5Z","block_id":"5","ack":false,"tail":"N425UA","flight":"UA1003","msgno":"M45A","text":"/B6 DFWEWR EWR R29"}')
    x.append('{"timestamp":1637698406.9086061,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-13,"error":0,"mode":"2","label":"_d","block_id":"6","ack":"T","tail":"N425UA","flight":"UA1003","msgno":"S14A"}')
    x.append('{"timestamp":1637698412.561126,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-13,"error":0,"mode":"2","label":"_d","block_id":"7","ack":"U","tail":"N425UA","flight":"UA1003","msgno":"S15A"}')
    x.append('{"timestamp":1637698418.787153,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-13,"error":0,"mode":"2","label":"_d","block_id":"8","ack":"V","tail":"N425UA","flight":"UA1003","msgno":"S16A"}')
    x.append('{"timestamp":1637698436.1538129,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-9,"error":0,"mode":"2","label":"15","block_id":"1","ack":false,"tail":"N810TA","flight":"GS0001","msgno":"M00A","text":"(2N41359W 81333OFF23112120111313--------(Z"}')
    x.append('{"timestamp":1637698773.7449961,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-14,"error":0,"mode":"2","label":"H2","block_id":"5","ack":false,"tail":"CFFJA","flight":"QK8753","msgno":"M10A","text":"02E23CYYZKCMHN43121W08014620042029M258335076B   QQ    N43043W08035220072468M310332083G   QQ    N42562W08057420102770M370337098G   QQ    N42475W08120620133019M430334097G   QQ    N42344W08141820163199M475329097G ","end":true}')
    x.append('{"timestamp":1637698793.0777061,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-14,"error":0,"mode":"2","label":"H2","block_id":"6","ack":false,"tail":"CFFJA","flight":"QK8753","msgno":"M10B","text":"  QQ    N42120W08153420193198M475330094G   QQ    "}')
    x.append('{"timestamp":1637699032.44766,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-15,"error":3,"mode":"2","label":"80","block_id":"7","ack":false,"tail":"CFFJA","flight":"QK8753","msgno":"M11A","text":"01,0D,DSPTCH,QK,8753,23,CYYZ,KCMH,..CFFJA\r\n202351,23NOV21,N41409,W082043,280\r\nASHLEY\r\nATC RE CLEARED\r\nUS DIRECT WAAHU\r\nCBUSS1 KCMH"}')
    x.append('{"timestamp":1637699318.4294519,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-17,"error":1,"mode":"2","label":"_d","block_id":"9","ack":"D","tail":"CFFJA","flight":"QK8753","msgno":"S37A"}')
    x.append('{"timestamp":1637699948.3995171,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-14,"error":0,"mode":"2","label":"H1","block_id":"6","ack":false,"tail":"N833UA","flight":"UA2375","msgno":"D52A","text":"#DFBA02/A31902,1,1/CCN833UA,NOV23,203256,KLGA,KDEN,2375/C106,06938,5000,96,0010,0,0100,96,X/CEN304,36006,259,781,1397,294,I73014/CNN303,36004,259,781,1396,294/EC011215,01215,00615,73,12,12/EE010690,01215,00615,","end":true}')
    x.append('{"timestamp":1637700604.907506,"station_id":"rpi-zero-1","channel":0,"freq":131.550,"level":-19,"error":3,"mode":"2","label":"Q0","block_id":"5","ack":false,"tail":"C-GITR","flight":"RV1673","msgno":"S23A"}')

    return x


sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sck.connect(('127.0.0.1', 5555))

data = loadTestData()


while True:

    for dataRec in data:
        msg = bytes(dataRec, 'utf-8')
        retry = True
        while (retry):
            try:
                sck.send(msg)
            except ConnectionRefusedError:
                time.sleep(1)
            except:
                time.sleep(1)
            else:
                retry = False

        time.sleep(2)

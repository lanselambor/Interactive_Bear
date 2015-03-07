# server

import socket
import time
import grovepi

input = 2
count = 0
# Connect the speaker to digital port D3
speaker = 3
grovepi.pinMode(speaker,"OUTPUT")
time.sleep(1)
i = 0

address = ('192.168.0.181', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()
s.bind(address)
s.listen(5)

ss, addr = s.accept()
#print 'got connected from',addr
#ss.send('byebye')
#ra = ss.recv(512)
#print ra

#ss.close()
#s.close()


while True:
    try:
        #Socket recieve 
        ra = ss.recv(4)
        if ra == 'bear':
            grovepi.digitalWrite(speaker,1)
       
        # Read resistance from Potentiometer
        i = grovepi.analogRead(input)
        if i >= 1020:
            count += 1
            if count == 100:
                count = 0
            print 'pizoe_value:'
            print i, count
            #speaker open
            grovepi.digitalWrite(speaker,1)
            #socket send
            ss.send('bear')

        else:
            #speaker close
            grovepi.digitalWrite(speaker,0)
        time.sleep(0.01)

    except IOError:
        ss.close()
        s.close()
        print "Error"

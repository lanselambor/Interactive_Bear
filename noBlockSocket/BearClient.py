# server

import socket
import time
import grovepi
import select

input = 2
count = 0
# Connect the speaker to digital port D3
speaker = 3
grovepi.pinMode(speaker,"OUTPUT")
#grovepi.pinMode(input,"INPUT")
time.sleep(1)
i = 0

address = ('192.168.21.205', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()
s.connect(address)

while True:
    try:
        #Not blocked socket
        infds, outfds, errfds = select.select([s,],[],[],1)
        #if infds changed, get to process, ignore if not changed
        if len(infds) != 0:
            buf = s.recv(4)
            if len(buf) != 0:
                print 'rev:', buf
                if buf == 'bear':
                    grovepi.digitalWrite(speaker,1)
                    time.sleep(3)
            print 'no data coming'

        # Read resistance from Potentiometer
        i = grovepi.analogRead(input)      
        if i >= 1020:
            time.sleep(0.05)
#        if grovepi.digitalRead(input) == 1: 
#            time.sleep(0.05)
            i = grovepi.analogRead(input)
            if i >= 1020:                    
#            if grovepi.digitalRead(input) == 1:
                count += 1
                if count == 100:
                    count = 0
                print 'speak:'
                print i, count
                #speaker open
                grovepi.digitalWrite(speaker,1)
                #socket send
                s.send('bear')
                time.sleep(0.5)
        else:
            #speaker close
            grovepi.digitalWrite(speaker,0)

    except IOError:
        s.close()
        print "Error"

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

address = ('192.168.21.205', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()
s.connet(address)

while True:
    try:
        #Socket recieve 
        data = s.recv(4)
        print 'the data received is',data

        if data == "bear":
            grovepi.digitalWrite(speaker,1)
            time.sleep(4)  # wait for bear speaking
        
        # Read resistance from Potentiometer
        i = grovepi.analogRead(input)
        if i >= 1020:
            time.sleep(0.05)
            i = grovepi.analogRead(input)
            if i >= 1020:                    
                count += 1
                if count == 100:
                    count = 0
                print 'speak:'
                print i, count
                #speaker open
                grovepi.digitalWrite(speaker,1)
                #socket send
                s.send('bear')
                time.sleep(4)
        else:
            #speaker close
            grovepi.digitalWrite(speaker,0)

    except IOError:
        s.close()
        print "Error"

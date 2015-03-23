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
grovepi.pinMode(input,"INPUT")
time.sleep(1)
i = 0

address = ('192.168.0.178', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()
s.bind(address)
s.listen(5)
#ss, addr = s.accept()


while True:
    try:
        #Not blocked socket
        infds, outfds, errfds = select.select([s,],[],[],1)
        #if infds changed, get to process, ignore if not changed
        if len(infds) != 0:
            ss, addr = s.accept()
            infds_c, outfds_c, errfds_c = select.select([ss],[],[],3)
            if len(infds_c) != 0:
                buf = ss.recv(4)
                if len(buf) != 0:
                    print buf
                    if buf == 'bear':
                        grovepi.digitalWrite(speaker,1)
                        time.sleep(4)
                    ss.close()    
            print 'no data coming'    

        # Read resistance from Potentiometer
        i = grovepi.analogRead(input)
        if i >= 1020:
#        if grovepi.digitalRead(input) == 1:
            time.sleep(0.05)
            i = grovepi.analogRead(input)
            if i >= 1020:                    
#            if grovepi.digitalRead(input) == 1:
                count += 1
                if count == 100:
                    count = 0
                print 'pizoe_value:'
                print i, count
                #speaker open
                grovepi.digitalWrite(speaker,1)
                #socket send
                ss.send('bear')
                time.sleep(0.5)
        else:
            #speaker close
            grovepi.digitalWrite(speaker,0)
        time.sleep(0.01)

    except IOError:
        ss.close()
        s.close()
        print "Error"

# client
import socket
import time
import grovepi
import socket



input = 2
count = 0
# Connect the speaker to digital port D3
speaker = 3
grovepi.pinMode(speaker,"OUTPUT")
time.sleep(1)
i = 0


address = ('192.168.0.181', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

#data = s.recv(512)
#print 'the data received is',data

#s.send('hihi')

#s.close()

while True:
    try:
        #Socket Recieve
        data = s.recv(4)
        print 'the data received is',data        
        
        if data == "bear":
            grovepi.digitalWrite(speaker,1)

        # Read resistance from Potentiometer
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

        else:
            #speaker close
            grovepi.digitalWrite(speaker,0)
        time.sleep(0.01)

    except IOError:
        s.close()
        print "Error"

import socket
import time
import threading
import thread
import signal
import sys
import grovepi

server_addr = ("45.62.100.29", 31500)

# def grovepi_init():
input = 7
count = 0
# output pin
speaker = 4
grovepi.pinMode(speaker, "OUTPUT")  
grovepi.pinMode(input, "INPUT")
time.sleep(1)

def io_actions(sock):   
    if 1 == grovepi.digitalRead(input):
        time.sleep(0.05)
	if 1 == grovepi.digitalRead(input):
	    print "HIGH"     
            grovepi.digitalWrite(speaker, 1) 
            sock.send("action")            
            time.sleep(3)
            grovepi.digitalWrite(speaker, 0) 
           
        
# Client

threadFlag = True
     
def recvThread(sock):
    global threadFlag
    while threadFlag:
	try:
	    cmd = sock.recv(1024)
	    print cmd 
	    if cmd == "action":
		print 'action'
                grovepi.digitalWrite(speaker, 1)
                time.sleep(4) 
                grovepi.digitalWrite(speaker, 0)
	except:
	    (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
	    print 'recv error: ', ErrorValue
	    threadFlag = False
	    
def sendThread(sock):
    global threadFlag
    while threadFlag:           
	print 'send...Hello'
	sock.send("Hello")
	sock.send("1")
	time.sleep(2)
        
# Socket work
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
#    sock.connect(('45.62.100.29', 31500))
    sock.connect(server_addr)
except socket.error, arg:
    (errno, err_msg) = arg
    print "Connect server failed: %s, errno=%d "%(err_msg, errno)
    sock.close()

thread.start_new_thread(recvThread, (sock, ))
#thread.start_new_thread(sendThread, (sock, ))

# main thread
while True:  
    io_actions(sock)
#    cmd = raw_input("input: ") 
#    print ''
#    sock.send(cmd)
#    time.sleep(1)

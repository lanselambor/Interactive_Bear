import socket
import time
import threading
import thread
import signal
import sys
import grovepi
import subprocess, os
import ITG3200


server_addr = ("45.62.100.29", 31500)

# ITG3200
gyro = ITG3200.ITG3200()
gyro.init()
gyro.zeroCalibrate(20, 20)
print "ITG3200 init OK."

def getShakingState():
    x_temp = 0
    for i in range(100):
        x, y, z = gyro.getAngularVelocity()
        x_temp += x
    x = x_temp / 100
#    print "ax = ",x
    if 2200 <= abs(x):
        return True
    return False

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
    if True == getShakingState():       
	sock.send("shaking")            
	grovepi.digitalWrite(speaker, 1) 
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
                time.sleep(3)
                grovepi.digitalWrite(speaker, 0)
	    if cmd == "shaking":
		print 'shaking..'
                grovepi.digitalWrite(speaker, 1)
                time.sleep(3)
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
    grovepi.digitalWrite(speaker, 1)
    time.sleep(3)
    grovepi.digitalWrite(speaker, 0)  
except socket.error, arg:
    (errno, err_msg) = arg
    sock.close()
    sys.exit()

thread.start_new_thread(recvThread, (sock, ))


# Signal "ctrl+c" interrupt
def do_exit(signalnum = None, handler = None):
    global threadFlag 
    threadFlag = False    
    time.sleep(1)
    sock.close()
    sys.exit()

signal.signal(signal.SIGINT, do_exit)    
signal.signal(signal.SIGHUP, do_exit)
signal.signal(signal.SIGQUIT, do_exit)

# main thread
while True:  
    io_actions(sock)
#    cmd = raw_input("input: ") 
#    print ''
#    sock.send(cmd)
#    time.sleep(1)

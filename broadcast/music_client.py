import socket
import time
import threading
import thread
import signal
import sys
import grovepi
import subprocess, os

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
                subprocess.Popen("omxplayer /home/pi/Interactive_Bear/MP3/Immortals.mp3", shell=True)
                time.sleep(4) 
                subprocess.Popen("python ./script/killAudio.py", shell=True)
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
    time.sleep(2)
    grovepi.digitalWrite(speaker, 0)  
except socket.error, arg:
    (errno, err_msg) = arg
    print "Connect server failed: %s, errno=%d "%(err_msg, errno)
    sock.close()

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

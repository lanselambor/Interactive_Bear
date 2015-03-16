import socket
import time
import threading
import thread
import signal
import sys

# Client

threadFlag = True
     
def recvThread(sock):
    global threadFlag
    while threadFlag:
	try:
	    rc = sock.recv(1024)
	    print rc 
	    if rc == "handTouch":
		print 'handTouch'
	    elif rc =='bodyShake':
		print 'bodyShake'
	    elif rc == 'Hello':
		print 'Hello'
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
    sock.connect(('localhost', 31500))
except socket.error, arg:
    (errno, err_msg) = arg
    print "Connect server failed: %s, errno=%d "%(err_msg, errno)
    sock.close()

thread.start_new_thread(recvThread, (sock, ))
#thread.start_new_thread(sendThread, (sock, ))

# main thread
while True:    
    sock.send("1")
    time.sleep(2)

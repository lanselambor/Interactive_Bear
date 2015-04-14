import subprocess
import time
import os

subprocess.Popen("mplayer /home/pi/Interactive_Bear/MP3/coming.mp3", shell=True)
time.sleep(2)
subprocess.Popen("pkill -9 mplayer", shell=True)


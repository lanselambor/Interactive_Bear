import subprocess
import time
import os

subprocess.Popen("omxplayer /home/pi/Interactive_Bear/MP3/Immortals.mp3", shell=True)
time.sleep(2)
subprocess.Popen("python ./killAudio.py", shell=True)



import subprocess
import time

# Start aplay
aplay_process = subprocess.Popen(["aplay", "long_siren.wav"])

# Keep playing until user inputs 0
code_run = 1
while code_run:
    code_run = int(input("Enter 0 stop audio: "))
    
# Stop aplay
aplay_process.terminate()
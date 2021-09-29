import os
import sys

os.system('pip3 install opencv-python')
os.system('pip3 install mediapipe')
os.system('pip3 install numpy')

if sys.platform == 'win32':
    os.system('copy nircmd.exe C:\\Windows')
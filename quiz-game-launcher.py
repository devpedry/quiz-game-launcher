import subprocess
import html
import requests
import random


GAME_PATH = r'E:\SteamLibrary\steamapps\common\War Thunder\launcher.exe' # Change this to your game launcher path


number = random.randint(1, 6) 
          
choice = int(input('type a number betwn 1 and 6. '))


if choice != number:
    print('You won..') 
    subprocess.Popen([GAME_PATH])
else: 
    subprocess.Popen(['shutdown', '/s', '/t', '10']) 
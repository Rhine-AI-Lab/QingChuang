from omxplayer.player import OMXPlayer
from pathlib import Path
import time

# 树莓派播放MP3音频文件
def play(path_str):
    path = Path(path_str)
    OMXPlayer(path)
    
play('./temp.mp3')
time.sleep(2)
print('finish')

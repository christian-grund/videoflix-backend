import subprocess
import os

# def convert_480p(source):
#     target = source + '_480p.mp4'
#     # cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
#     cmd = 'ffmpeg -i "breakout.mp4" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "breakout_480p.mp4"'
#     subprocess.run(cmd)

def convert_480p(source):
    ffmpeg_path = '/Users/christian/usr/ffmpeg/ffmpeg'  # Vollständiger Pfad
    base, ext = os.path.splitext(source)
    target = base + '_480p' + ext
    cmd = '{} -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(ffmpeg_path, source, target)
    subprocess.run(cmd, shell=True)


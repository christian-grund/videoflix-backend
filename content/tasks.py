import subprocess
import os

def convert_video(source, resolution, scale):
    ffmpeg_path = '/Users/christian/usr/ffmpeg/ffmpeg'  # Vollständiger Pfad
    base, ext = os.path.splitext(source)
    target = base + '{}'.format(resolution) + ext
    cmd = '{} -i "{}" -vf {} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(ffmpeg_path, source, scale, target)
    subprocess.run(cmd, shell=True)

def convert_360p(source):
    ffmpeg_path = '/Users/christian/usr/ffmpeg/ffmpeg'  # Vollständiger Pfad
    base, ext = os.path.splitext(source)
    target = base + '_360p' + ext
    cmd = '{} -i "{}" -vf "scale=640:360" -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(ffmpeg_path, source, target)
    subprocess.run(cmd, shell=True)


def convert_720p(source):
    ffmpeg_path = '/Users/christian/usr/ffmpeg/ffmpeg'  # Vollständiger Pfad
    base, ext = os.path.splitext(source)
    target = base + '_720p' + ext
    cmd = '{} -i "{}" -vf "scale=1280:720" -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(ffmpeg_path, source, target)
    subprocess.run(cmd, shell=True)


def convert_1080p(source):
    ffmpeg_path = '/Users/christian/usr/ffmpeg/ffmpeg'  # Vollständiger Pfad
    base, ext = os.path.splitext(source)
    target = base + '_1080p' + ext
    cmd = '{} -i "{}" -vf "scale=1920:1080" -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(ffmpeg_path, source, target)
    subprocess.run(cmd, shell=True)



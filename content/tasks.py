import subprocess
import os

def convert_video(source, resolution, scale):
    ffmpeg_path = '/Users/christian/usr/ffmpeg/ffmpeg'  # Vollständiger Pfad
    base, ext = os.path.splitext(source)
    target = base + '{}'.format(resolution) + ext
    cmd = '{} -i "{}" -vf {} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(ffmpeg_path, source, scale, target)
    subprocess.run(cmd, shell=True)


def create_video_screenshot(video_path, output_image_path, time="00:00:05"):
    """
    Erstellt einen Screenshot eines Videos mit ffmpeg.
    """
    # time.sleep(5)  # 10 Sekunden warten
    if not os.path.exists(video_path):
        print(f"Video-Datei nicht gefunden: {video_path}")
        return

    # Kurze Verzögerung, um sicherzustellen, dass die Datei verfügbar ist
    

    try:
        command = [
            'ffmpeg',
            '-ss', time,
            '-i', video_path,
            '-vframes', '1',
            '-q:v', '2',
            output_image_path
        ]
        subprocess.run(command, check=True)
        print(f'Screenshot erstellt: {output_image_path}')
    except subprocess.CalledProcessError as e:
        print(f'Fehler bei der Screenshot-Erstellung: {e}')


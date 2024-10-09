import os
import subprocess
import textwrap


def convert_video(source, resolution, scale):
    ffmpeg_path = '/Users/christian/usr/ffmpeg/ffmpeg'  # Vollständiger Pfad
    base, ext = os.path.splitext(source)
    target = base + '{}'.format(resolution) + ext
    cmd = '{} -i "{}" -vf {} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(ffmpeg_path, source, scale, target)
    subprocess.run(cmd, shell=True)


def create_video_screenshot(video_path, output_image_path, time="00:00:05"):

    if not os.path.exists(video_path):
        print(f"Video-Datei nicht gefunden: {video_path}")
        return    
    
    # Überprüfen, ob das Zielbild bereits existiert und es löschen
    print(f'output_image_path: {output_image_path}')
    if os.path.isfile(output_image_path):
        os.remove(output_image_path)
        print(f'Vorhandene Screenshot-Datei gelöscht: {output_image_path}')

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



def delete_original_video(video_path):
    if os.path.isfile(video_path):
        os.remove(video_path)


def delete_original_screenshot(screenshot_with_text_path):
    if os.path.isfile(screenshot_with_text_path):
        os.remove(screenshot_with_text_path)

# def delete_original_screenshot(screenshot_with_text_path):
#     print(f'delete_screenshot_with_text: {screenshot_with_text_path}')
#     if os.path.isfile(screenshot_with_text_path):
#         os.remove(screenshot_with_text_path)

def delete_screenshot_with_text(screenshot_with_text_path):
    print(f'delete_screenshot_with_text: {screenshot_with_text_path}')
    if os.path.isfile(screenshot_with_text_path):
        os.remove(screenshot_with_text_path)


def create_thumbnail_with_text(image_path, video_title, fontsize=145, max_chars_per_line=25):
    def split_text_by_length(text, max_len):
        return '\n'.join(textwrap.wrap(text, max_len))

    formatted_text = split_text_by_length(video_title, max_chars_per_line)

    output_image_path_with_text = os.path.splitext(image_path)[0] + '_with_text.jpg'
    print('output_image_path_with_text:', output_image_path_with_text)
    print('formatted_text:', formatted_text)

    try:
        y_position = f"h-(text_h*1.5)"

        command = [
            'ffmpeg',
            '-i', image_path,
            '-vf', f"drawtext=text='{formatted_text}':fontcolor=white:fontsize={fontsize}:x=(w-text_w)/2:y={y_position}",
            output_image_path_with_text
        ]
        subprocess.run(command, check=True)
        print(f'Thumbnail mit Text erstellt: {output_image_path_with_text}')
    except subprocess.CalledProcessError as e:
        print(f'Fehler bei der Erstellung des Thumbnails mit Text: {e}')

    return output_image_path_with_text














import os
import subprocess
import textwrap
import shutil

from videoflix import settings


def convert_video(source, resolution, scale):
    """
    Converts a video file to a specified resolution using FFmpeg.
    """
    if not os.path.exists(source):
        raise FileNotFoundError(f"Source file '{source}' does not exist.")
    
    # ffmpeg_path = '/Users/christian/usr/ffmpeg/ffmpeg'  
    ffmpeg_path = '/usr/bin/f(fmpeg'  
    base, ext = os.path.splitext(source)

    temp_target = os.path.join(settings.MEDIA_ROOT, 'temp_videos', f"{os.path.basename(base)}_{resolution}{ext}")
    final_target = os.path.join(settings.MEDIA_ROOT, 'videos', f"{os.path.basename(base)}_{resolution}{ext}")
    
    # Ensure temp_videos directory exists
    os.makedirs(os.path.dirname(temp_target), exist_ok=True)
    
    cmd = '{} -i "{}" -vf {} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(ffmpeg_path, source, scale, temp_target)
    subprocess.run(cmd, shell=True)

    # Move the file to the final directory once conversion is done
    shutil.move(temp_target, final_target)

    # target = base + '{}'.format(resolution) + ext
    # cmd = '{} -i "{}" -vf {} -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(ffmpeg_path, source, scale, target)
    # subprocess.run(cmd, shell=True)


def create_video_screenshot(video_path, output_image_path, time="00:00:05"):
    """
    Creates a screenshot from a video at a specified time using FFmpeg.
    """
    if not os.path.exists(video_path):
        return 

    if os.path.exists(output_image_path):
        return    

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
    except subprocess.CalledProcessError as e:
        print(f'Fehler bei der Screenshot-Erstellung: {e}')



def delete_original_video(video_path):
    """
    Deletes the original video file if it exists.
    """
    if os.path.isfile(video_path):
        os.remove(video_path)


def delete_original_screenshot(screenshot_with_text_path):
    """
    Deletes the original screenshot file if it exists.
    """
    if os.path.isfile(screenshot_with_text_path):
        os.remove(screenshot_with_text_path)


def delete_screenshot_with_text(screenshot_with_text_path):
    """
    Deletes a screenshot with text overlay if it exists.
    """
    if os.path.isfile(screenshot_with_text_path):
        os.remove(screenshot_with_text_path)


def create_thumbnail_with_text(image_path, video_title, fontsize=145, max_chars_per_line=25):
    """
    Creates a thumbnail image from the specified image file, overlaying the video title as text.
    """
    def split_text_by_length(text, max_len):
        return '\n'.join(textwrap.wrap(text, max_len))

    formatted_text = split_text_by_length(video_title, max_chars_per_line)

    output_image_path_with_text = os.path.splitext(image_path)[0] + '_with_text.jpg'

    try:
        y_position = f"h-(text_h*1.5)"

        command = [
            'ffmpeg',
            '-i', image_path,
            '-vf', f"drawtext=text='{formatted_text}':fontcolor=white:fontsize={fontsize}:x=(w-text_w)/2:y={y_position}",
            output_image_path_with_text
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Fehler bei der Erstellung des Thumbnails mit Text: {e}')

    return output_image_path_with_text

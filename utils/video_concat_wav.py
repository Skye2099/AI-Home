'''
@File    :   video_concat_wav.py
@Time    :   2024/06/17 17:18:34
@Author  :   skye 
@Desc    :   concat videos and wavs
'''
import os 
import subprocess


def get_all_files(directory, extension):
    """get files by traversal dir

    Args:
        directory (string): _description_
        extension (string): _description_

    Returns:
        _type_: _description_
    """
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                files.append(os.path.join(root, filename))

    return files

def merge_video_audio(video_file, audio_file, output_file):
    """ use 'pip install ffmpeg' to easy install ffmpeg

    Args:
        video_file (_type_): _description_
        audio_file (_type_): _description_
        output_file (_type_): _description_
    """
    command = [
        'ffmpeg', '-i', video_file, '-i', audio_file,
        '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
        output_file
    ]
    subprocess.run(command)

def main(video_dir, audio_dir, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    video_files = get_all_files(video_dir, '.mp4')
    audio_files = get_all_files(audio_dir, '.wav')

    for video_file in video_files:
        video_name = os.path.splitext(os.path.basename(video_file))[0]
        matching_audio_file = next((audio_file for audio_file in audio_files if os.path.splitext(os.path.basename(audio_file))[0] == video_name), None)

        if matching_audio_file:
            output_file = os.path.join(output_dir, video_name + '_merged.mp4')
            merge_video_audio(video_file, matching_audio_file, output_file)
            print(f'Merged: {video_file} and {matching_audio_file} into {output_file}')
        else:
            print('No matching audio file for video: {video_file}')


if __name__ == '__main__':
    video_dir = '/root/wts/data/concat_video/video'
    audio_dir = '/root/wts/data/concat_video/audio'
    output_dir = '/root/wts/data/concat_video/output'

    main(video_dir, audio_dir, output_dir)

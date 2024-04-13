import os
import subprocess

import folder_paths

from .util import get_ffmpeg_path


video_extensions = ['webm', 'mp4', 'mkv']

def get_audio(video, start_time=0, duration=0):
    ffmpeg_path = get_ffmpeg_path()
    args = [ffmpeg_path, "-v", "error", "-i", video]
    if start_time > 0:
        args += ["-ss", str(start_time)]
    if duration > 0:
        args += ["-t", str(duration)]
    try:
        res = subprocess.run(
            args + ["-f", "wav", "-"],
            stdout=subprocess.PIPE,
            check=True
        ).stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to extract audio from: {video}")
    return res

class LoadVideoAudioNode:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = os.listdir(input_dir)
        files = filter(lambda f: os.path.isfile(os.path.join(input_dir, f)), files)
        files = filter(lambda f: os.path.splitext(f)[1].lstrip('.') in video_extensions, files)
        return {
            "required": {
                "video": (sorted(files),),
            },
        }

    CATEGORY = "audio"

    RETURN_TYPES = ("WAV_BYTES", )
    RETURN_NAMES = ("wav_bytes", )

    FUNCTION = "load_video_audio"

    def load_video_audio(self, video):
        input_directory = folder_paths.get_input_directory()
        filepath = os.path.join(input_directory, video)
        audio = get_audio(filepath)
        return (audio, )

    # @classmethod
    # def IS_CHANGED(cls, video, **kwargs):
    #     image_path = folder_paths.get_annotated_filepath(video)
    #     return calculate_file_hash(image_path)

    @classmethod
    def VALIDATE_INPUTS(cls, video, **kwargs):
        if not folder_paths.exists_annotated_filepath(video):
            return "Invalid video file: {}".format(video)
        return True

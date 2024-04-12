import os
import subprocess

import folder_paths
import logging
# from .utils import BIGMAX, DIMMAX, calculate_file_hash, get_sorted_dir_files_from_directory, get_audio, lazy_eval, hash_path, validate_path
from .util import get_ffmpeg_path


video_extensions = ['webm', 'mp4', 'mkv', 'gif']

# get_audio(video, skip_first_frames * target_frame_time,
#                                frame_load_cap*target_frame_time*select_every_nth)
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
            # "hidden": {
            #     "unique_id": "UNIQUE_ID"
            # },
        }

    CATEGORY = "Example"

    RETURN_TYPES = ("wav_bytes", )
    RETURN_NAMES = ("wav_bytes", )

    FUNCTION = "test"

    def test(self, video):
        input_directory = folder_paths.get_input_directory()
        filepath = os.path.join(input_directory, video)
        audio = get_audio(filepath)
        print('\n\n\n')
        print(type(audio))
        print('\n\n\n')
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

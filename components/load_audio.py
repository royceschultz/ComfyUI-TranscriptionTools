import os

import folder_paths

from .util import get_wav_bytes_from_file, audio_extensions


class LoadAudioNode:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = os.listdir(input_dir)
        files = filter(lambda f: os.path.isfile(os.path.join(input_dir, f)), files)
        files = filter(lambda f: os.path.splitext(f)[1].lstrip('.') in audio_extensions, files)
        return {
            "required": {
                "audio": (sorted(files),),
            },
        }

    CATEGORY = "audio"

    RETURN_TYPES = ("WAV_BYTES", )
    RETURN_NAMES = ("wav_bytes", )

    FUNCTION = "load_audio"

    def load_audio(self, audio):
        input_directory = folder_paths.get_input_directory()
        filepath = os.path.join(input_directory, audio)
        audio = get_wav_bytes_from_file(filepath)
        return (audio, )

    # @classmethod
    # def IS_CHANGED(cls, video, **kwargs):
    #     image_path = folder_paths.get_annotated_filepath(video)
    #     return calculate_file_hash(image_path)

    @classmethod
    def VALIDATE_INPUTS(cls, audio, **kwargs):
        if not folder_paths.exists_annotated_filepath(audio):
            return "Invalid video file: {}".format(audio)
        return True

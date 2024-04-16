import os
import re

import folder_paths

from .util import get_wav_bytes_from_file, audio_extensions, video_extensions


accepted_extensions = audio_extensions + video_extensions

class LoadBatchNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_folder": (['input', 'root'],),
                "path": ("STRING", {"default": ""}),
                "regex_match": ("STRING", {"default": ""}),
                "regex_exclude": ("STRING", {"default": ""}),
            },
        }

    CATEGORY = "audio"

    RETURN_TYPES = ("WAV_BYTES_BATCH", "INT", "LIST[STRING]")
    RETURN_NAMES = ("wav_bytes_batch", "count", "filenames")

    FUNCTION = "load_audio"

    def load_audio(self, base_folder, path, regex_match, regex_exclude):
        base_dir = None
        if base_folder == 'input':
            base_dir = folder_paths.get_input_directory()
        elif base_folder == 'root':
            base_dir = ""
        path_dir = os.path.join(base_dir, path)
        assert os.path.exists(path_dir), f"Path {path_dir} does not exist"
        assert os.path.isdir(path_dir), f"Path {path_dir} is not a directory"
        files = os.listdir(path_dir)
        files = filter(lambda f: os.path.isfile(os.path.join(path_dir, f)), files)
        files = filter(lambda f: os.path.splitext(f)[1].lstrip('.') in accepted_extensions, files)
        if regex_match:
            files = filter(lambda f: re.search(regex_match, f), files)
        if regex_exclude:
            files = filter(lambda f: not re.search(regex_exclude, f), files)
        files = list(files)
        audio_batch = []
        for f in files:
            filepath = os.path.join(path_dir, f)
            item = {
                "filename": f,
                "file_path": filepath,
            }
            # Need to initialize get_audio this way because of the way references are handled.
            # Something to do with closures and late binding.
            # Else get_audio will always refer to the last item in the loop.
            item["get_audio"] = lambda x=filepath: get_wav_bytes_from_file(x)

            audio_batch.append(item)
        return (audio_batch, len(audio_batch), list(files))

    # @classmethod
    # def IS_CHANGED(cls, video, **kwargs):
    #     image_path = folder_paths.get_annotated_filepath(video)
    #     return calculate_file_hash(image_path)

    # @classmethod
    # def VALIDATE_INPUTS(cls, audio, **kwargs):
    #     if not folder_paths.exists_annotated_filepath(audio):
    #         return "Invalid video file: {}".format(audio)
    #     return True

import os
import re
import time
# ComfyUI imports
import folder_paths
# Local imports
from .util import increment_filename_no_overwrite

class AudioSinkNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "wav_bytes": ("wav_bytes",),
                "filename": ("STRING", {"default": "AudioSink"}),
                "save_format": (['wav'],),
                "save_output": ("BOOLEAN", {"default": True}),
                "overwrite_existing": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = tuple()
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "test"

    OUTPUT_NODE = True

    CATEGORY = "Example"

    def test(self, wav_bytes, filename, save_format, save_output, overwrite_existing):
        if not save_output:
            return (1, )

        filename = filename.strip()
        assert filename, "Filename cannot be empty"

        base_output_dir = folder_paths.get_output_directory()
        assert os.path.exists(base_output_dir), f"Output directory {base_output_dir} does not exist"
        output_dir = os.path.join(base_output_dir, 'audio')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename + '.' + save_format)

        if os.path.exists(output_path) and not overwrite_existing:
            output_path = increment_filename_no_overwrite(output_path)

        with open(output_path, 'wb') as f:
            f.write(wav_bytes)
        return (0, )

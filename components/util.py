import os
import re
import shutil

def increment_filename_no_overwrite(proposed_path):
    output_dir, filename_ext = os.path.split(proposed_path)
    filename, file_format = os.splitext(filename_ext)
    files = os.listdir(output_dir)
    files = filter(lambda f: os.path.isfile(os.path.join(output_dir, f)), files)
    files = filter(lambda f: f.startswith(filename), files)
    files = filter(lambda f: f.endswith('.' + file_format), files)
    file_numbers = [re.search(r'_(\d+)\.', f) for f in files]
    file_numbers = [int(f.group(1)) for f in file_numbers if f]
    this_file_number = max(file_numbers) + 1 if file_numbers else 1
    output_path = os.path.join(output_dir, filename + f'_{this_file_number}.' + file_format)
    return output_path


def get_ffmpeg_path():
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg is not None:
        return system_ffmpeg
    raise FileNotFoundError("No valid ffmpeg found.")

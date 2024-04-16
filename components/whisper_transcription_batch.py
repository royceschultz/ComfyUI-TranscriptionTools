import os
import sys
from tqdm import tqdm

import comfy.utils
import folder_paths

from .util import increment_filename_no_overwrite

def format_transcription(result, format_newlines_on_punctuation):
    text = result["text"]
    if format_newlines_on_punctuation:
        punct = ['.', '?', '!']
        for p in punct:
            text = text.replace(f'{p} ', f'{p}\n')
    return text

def format_chunks(chunks):
    format_chunk = lambda chunk: f'{chunk["timestamp"][0]}, {chunk["timestamp"][1]}, {chunk["text"]}'
    return '\n'.join([format_chunk(chunk) for chunk in chunks])


class WhisperTranscriptionBatchNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipeline": ('TRANSCRIPTION_PIPELINE',),
                "wav_bytes_batch": ('WAV_BYTES_BATCH',),
                "format_newlines_on_punctuation": ('BOOLEAN', {'default': True}),
                "save_transcription": ('BOOLEAN', {'default': False}),
                "save_chunks": ('BOOLEAN', {'default': False}),
                "filename_prefix": ('STRING', {'default': ''}),
                "filename_suffix": ('STRING', {'default': ''}),
                "overwrite_existing": ('BOOLEAN', {'default': True}),
            },
        }

    RETURN_TYPES = tuple()
    RETURN_NAMES = tuple()

    FUNCTION = "transcribe"

    CATEGORY = "transcription"

    OUTPUT_NODE = True

    def transcribe(
        self, pipeline, wav_bytes_batch,
        format_newlines_on_punctuation,
        save_transcription, save_chunks,
        filename_prefix, filename_suffix, overwrite_existing,
    ):
        errors = []

        base_output_dir = folder_paths.get_output_directory()
        assert os.path.exists(base_output_dir), f"Output directory {base_output_dir} does not exist"
        output_dir = os.path.join(base_output_dir, 'transcriptions')
        os.makedirs(output_dir, exist_ok=True)

        pbar = comfy.utils.ProgressBar(len(wav_bytes_batch))
        for item in tqdm(wav_bytes_batch, file=sys.stdout):
            filename = os.path.splitext(item['filename'])[0]
            save_filename = filename_prefix + filename + filename_suffix
            wav_bytes = item['get_audio']()
            tqdm.write(f'Starting Transcription for {filename}')
            try:
                result = pipeline(wav_bytes)
            except Exception as e:
                errors.append({
                    "filename": filename,
                    "error": str(e),
                })
                tqdm.write(str(e))
                continue
            else:
                if save_transcription:
                    transcription = format_transcription(result, format_newlines_on_punctuation)
                    transcription_path = os.path.join(output_dir, save_filename + '.txt')
                    if not overwrite_existing and os.path.exists(transcription_path):
                        transcription_path = increment_filename_no_overwrite(transcription_path)
                    with open(transcription_path, 'w') as f:
                        f.write(transcription)

                if save_chunks:
                    chunks = format_chunks(result['chunks'])
                    chunks_path = os.path.join(output_dir, save_filename + '_chunks.csv')
                    if not overwrite_existing and os.path.exists(chunks_path):
                        chunks_path = increment_filename_no_overwrite(chunks_path)
                    with open(chunks_path, 'w') as f:
                        f.write('start,stop,text\n')
                        f.write(chunks)
            finally:
                pbar.update(1)

        if errors:
            error_message = f'Some files failed to transcribe ({len(errors)} of {len(wav_bytes_batch)}):\n'
            for error in errors:
                error_message += f'{error["filename"]}: {error["error"]}\n'
            raise Exception(error_message)

        return tuple()

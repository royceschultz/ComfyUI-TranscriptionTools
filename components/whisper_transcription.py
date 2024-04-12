import folder_paths
import os

from .util import increment_filename_no_overwrite

class WhisperTranscriptionNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipeline": ('transcription_pipeline',),
                "wav_bytes": ('wav_bytes',),
                "format_newlines_on_punctuation": ('BOOLEAN', {'default': True}),
                "save_transcription": ('BOOLEAN', {'default': False}),
                "save_chunks": ('BOOLEAN', {'default': False}),
                "save_filename": ('STRING', {'default': 'transcription'}),
                "overwrite_existing": ('BOOLEAN', {'default': True}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", )
    RETURN_NAMES = ("transcription", "chunks")

    FUNCTION = "test"

    CATEGORY = "Example"

    OUTPUT_NODE = True

    def test(
        self, pipeline, wav_bytes,
        format_newlines_on_punctuation,
        save_transcription, save_chunks,
        save_filename, overwrite_existing,
    ):
        print('Starting Transcription')
        result = pipeline(wav_bytes)
        print('Transcription Done')
        text = result["text"]
        if format_newlines_on_punctuation:
            punct = ['.', '?', '!']
            for p in punct:
                text = text.replace(f'{p} ', f'{p}\n')
        format_chunks = lambda chunk: f'{chunk["timestamp"][0]}, {chunk["timestamp"][1]}, {chunk["text"]}'
        chunks = [format_chunks(chunk) for chunk in result['chunks']]
        chunks = '\n'.join(chunks)

        if save_transcription or save_chunks:
            base_output_dir = folder_paths.get_output_directory()
            assert os.path.exists(base_output_dir), f"Output directory {base_output_dir} does not exist"
            output_dir = os.path.join(base_output_dir, 'transcriptions')
            os.makedirs(output_dir, exist_ok=True)
            if save_transcription:
                transcription_path = os.path.join(output_dir, save_filename + '.txt')
                if os.path.exists(transcription_path) and not overwrite_existing:
                    transcription_path = increment_filename_no_overwrite(transcription_path)
                with open(transcription_path, 'w') as f:
                    f.write(text)

            if save_chunks:
                chunks_path = os.path.join(output_dir, save_filename + '_chunks.csv')
                if os.path.exists(chunks_path) and not overwrite_existing:
                    chunks_path = increment_filename_no_overwrite(chunks_path)
                with open(chunks_path, 'w') as f:
                    f.write('start,stop,text\n')
                    f.write(chunks)

        return (text, chunks)

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

class LoadWhisperModelNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'model_id': (['openai/whisper-large-v3'],),
                'language': (['en', 'auto'],),
            },
        }

    RETURN_TYPES = ('transcription_pipeline', )
    RETURN_NAMES = ('pipeline', )

    FUNCTION = 'test'

    CATEGORY = 'Example'

    def test(self, model_id, language):
        # from datasets import load_dataset
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model_id = 'openai/whisper-large-v3'

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )

        processor = AutoProcessor.from_pretrained(model_id)

        model.to(device)

        generate_kwargs = {}
        if language != 'auto':
            generate_kwargs['language'] = language

        pipe = pipeline(
            'automatic-speech-recognition',
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=torch_dtype,
            device=device,
            generate_kwargs=generate_kwargs,
        )

        return (pipe, )
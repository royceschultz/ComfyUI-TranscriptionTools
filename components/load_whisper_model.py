import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

model_ids = [
    'openai/whisper-large-v3',
    'openai/whisper-large-v2',
    'openai/whisper-large',
    'openai/whisper-medium',
    'openai/whisper-small',
    'openai/whisper-base',
    'openai/whisper-tiny',
    'openai/whisper-medium.en',
    'openai/whisper-small.en',
    'openai/whisper-base.en',
    'openai/whisper-tiny.en',
]

languages = ['en', 'auto', 'fr']

class LoadWhisperModelNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            'required': {
                'model_id': (model_ids,),
                'language': (languages,),
            },
        }

    RETURN_TYPES = ('TRANSCRIPTION_PIPELINE', )
    RETURN_NAMES = ('pipeline', )

    CATEGORY = 'transcription'

    FUNCTION = 'load_model'

    def load_model(self, model_id, language):
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        processor = AutoProcessor.from_pretrained(model_id)
        model.to(device)

        generate_kwargs = {}
        if language != 'auto':
            if model_id.endswith('.en'):
                if language != 'en':
                    raise ValueError(f'Model {model_id} only supports English language')
            else:
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

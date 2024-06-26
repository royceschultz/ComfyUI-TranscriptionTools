from .components.audio_sink_node import AudioSinkNode
from .components.load_whisper_model import LoadWhisperModelNode
from .components.whisper_transcription import WhisperTranscriptionNode
from .components.whisper_transcription_batch import WhisperTranscriptionBatchNode
from .components.load_video_audio import LoadVideoAudioNode
from .components.load_audio import LoadAudioNode
from .components.load_batch import LoadBatchNode

from .components.convert.vhs_audio_to_audio import VHSAudioToWavBytesNode

# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
# WEB_DIRECTORY = "./somejs"

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "TT-AudioSink": AudioSinkNode,
    "TT-LoadWhisperModel": LoadWhisperModelNode,
    "TT-WhisperTranscription": WhisperTranscriptionNode,
    "TT-WhisperTranscriptionBatch": WhisperTranscriptionBatchNode,
    "TT-ConvertVhsAudioToAudio": VHSAudioToWavBytesNode,
    "TT-LoadVideoAudio": LoadVideoAudioNode,
    "TT-LoadAudio": LoadAudioNode,
    "TT-LoadBatch": LoadBatchNode,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "TT-AudioSink": "Audio Sink",
    "TT-LoadWhisperModel": "Load Whisper Transcription Model",
    "TT-WhisperTranscription": "Whisper Transcribe",
    "TT-WhisperTranscriptionBatch": "Whisper Transcribe Batch",
    "TT-ConvertVhsAudioToAudio": "Convert VHS Audio to WAV bytes",
    "TT-LoadVideoAudio": "Load Audio from Video",
    "TT-LoadAudio": "Load Audio",
    "TT-LoadBatch": "Load Audio from Batch",
}

WEB_DIRECTORY = "./web"

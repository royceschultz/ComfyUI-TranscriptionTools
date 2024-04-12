from .components.audio_sink_node import AudioSinkNode
from .components.load_whisper_model import LoadWhisperModelNode
from .components.whisper_transcription import WhisperTranscriptionNode
from .components.load_video_audio import LoadVideoAudioNode

from .components.convert.vhs_audio_to_audio import VHSAudioToWavBytes

# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
# WEB_DIRECTORY = "./somejs"

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ExampleAudioSink": AudioSinkNode,
    "ExampleLoadWhisperModel": LoadWhisperModelNode,
    "ExampleWhisperTranscription": WhisperTranscriptionNode,
    "ConvertVhsAudioToAudio": VHSAudioToWavBytes,
    "ExampleLoadVideoAudio": LoadVideoAudioNode,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Example": "Example Node"
    # "ExampleAudioSink": "Audio Sink Node"
}

WEB_DIRECTORY = "./web"

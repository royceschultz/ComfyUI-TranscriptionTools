class VHSAudioToWavBytesNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "vhs_audio": ('VHS_AUDIO',),
            },
        }

    RETURN_TYPES = ("WAV_BYTES", )
    RETURN_NAMES = ("wav_bytes", )

    FUNCTION = "convert"

    CATEGORY = "audio"

    def convert(self, vhs_audio):
        return (vhs_audio(), )

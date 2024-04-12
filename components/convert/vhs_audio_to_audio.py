class VHSAudioToWavBytes:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "vhs_audio": ('VHS_AUDIO',),
            },
        }

    RETURN_TYPES = ("wav_bytes", )
    RETURN_NAMES = ("wav_bytes", )

    FUNCTION = "test"

    CATEGORY = "Example"

    def test(self, vhs_audio):
        return (vhs_audio(), )

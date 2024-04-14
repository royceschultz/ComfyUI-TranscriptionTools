# ComfyUI Transcription Tools (Under Development)

This package provides custom nodes for ComfyUI to perform transcription tasks on audio and video file inputs.

<img src="assets/workflow_example.jpg" alt="isolated" width="800"/>

Note: To text (Debug) is part of [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager), but you probably have that installed already.

## Transcription Models

[openai/whisper-large-v3](https://huggingface.co/openai/whisper-large-v3)

More models to be added in the future.

## Info

Video input is selected from the `input/` folder.

When the save options are selected transcriptions are stored in the `output/transcriptions/` directory. Transcription text is the full text of the transcription. Chunks output is a csv containing timestamp info for each chunk of the transcription.

## Special Thanks

The team supporting [ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite) which provided insrumental examples in the development of this tool.

# Nodes

## Input Nodes

### Load Audio

Load an audio file from the `input/` folder.

### Load Audio from Video

Load the audio component of a video file from the `input/` folder.

## Model Nodes

### Load Whisper Model
Create a new whisper pipeline to transcribe audio. Supports selecting the input language.

Note: Automatic language detection can occaisionally produce errors. If you're having trouble, try specifying the language manually.


## Processing Nodes

### Whisper Transcribe
Transcribe the audio using the whisper model. Includes options for saving files to the `output/transcription` folder.

## Output Nodes

### Audio Sink
Saves wav_bytes to a file in the `output/audio` folder. I only created this for debugging purposes.

## Utility Nodes

### Convert VHS Audio to WAV bytes

Converts audio from [Video Helper Suite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite) audio type to wav_bytes type. VHS is using wav_bytes under the hood, but currently the way ComfyUI handles type checking, it's necessary to convert it by name using this node.

**Conversion like this is not recommended for even mildly long input videos.** The VHS node is primarily to load the frames of videos, requiring significant memory usage for the image data. Long videos may OOM or at least take a LONG time.

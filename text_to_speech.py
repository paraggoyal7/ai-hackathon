import os
import wave
import numpy as np
from TTS.api import TTS


def text_to_speech(text_array, speaker1="p328", speaker2="p226", output_file="final_output.wav"):
    # Load a lighter multi-speaker TTS model
    model = "tts_models/en/vctk/vits"
    tts = TTS(model)

    temp_files = []

    for i, text in enumerate(text_array):
        temp_file = f"temp_{i}.wav"
        speaker = speaker1 if i % 2 == 0 else speaker2

        tts.tts_to_file(text=text, speaker=speaker, file_path=temp_file)
        temp_files.append(temp_file)
        print(f"Generated: {temp_file} with {speaker}")

    # Merge all temporary files into one
    merge_audio_files(temp_files, output_file)

    # Cleanup temporary files
    for file in temp_files:
        os.remove(file)

    print(f"Final output saved as {output_file}")
    return output_file


def merge_audio_files(file_list, output_file):
    data = []

    for file in file_list:
        with wave.open(file, "rb") as wav_file:
            if not data:
                params = wav_file.getparams()
            data.append(wav_file.readframes(wav_file.getnframes()))

    with wave.open(output_file, "wb") as output_wav:
        output_wav.setparams(params)
        for frames in data:
            output_wav.writeframes(frames)


if __name__ == "__main__":
    text_samples = [
        "Hello, how are you?",
        "I am fine, thank you!",
        "What about you?",
        "I am doing well too."
    ]
    text_to_speech(text_samples, speaker1="p225", speaker2="p226")

from pyAudioAnalysis import ShortTermFeatures as aF
from pyAudioAnalysis import audioBasicIO as aIO
from pydub import AudioSegment
import numpy as np

mp3_file = "/Users/parag/Downloads/every_tech_support_call_ever.mp3"
wav_file = "../customer_call.wav"
def convert_mp3_to_wav(mp3_file, wav_file):
    """
    Converts an MP3 file to WAV format using pydub.
    """
    audio = AudioSegment.from_mp3(mp3_file)
    audio = audio.set_channels(1)
    audio.export(wav_file, format="wav")
    print(f"Conversion complete! WAV file saved as: {wav_file}")


def detect_deviations(pitch_threshold=150, energy_threshold=0.5, window_size=1.0, step_size=0.5):
    """
    Analyzes the audio file for deviations in pitch and energy levels using short-term features.

    Args:
    - wav_file: Path to the WAV file
    - pitch_threshold: The threshold for pitch (Hz) to classify high pitch/angry tone
    - energy_threshold: The threshold for energy to classify loud/high energy tone
    - window_size: Window size for feature extraction (seconds)
    - step_size: Step size for feature extraction (seconds)

    Returns:
    - A list of time intervals (timestamps) where significant deviations occur.
    """
    # Step 1: Read audio data from the file
    fs, s = aIO.read_audio_file(wav_file)

    # Step 2: Extract short-term features
    win, step = window_size, step_size
    features, feature_names = aF.feature_extraction(s, fs, int(fs * win), int(fs * step))

    # Step 3: Get the energy and spectral centroid (which serves as a basic approximation of pitch)
    print(feature_names)
    energy = features[feature_names.index('energy'), :]
    spectral_centroid = features[feature_names.index('spectral_centroid'), :]

    # Step 4: Detect deviations based on the energy and spectral centroid thresholds
    timestamps = []
    duration = len(s) / float(fs)  # in seconds
    time = np.arange(0, duration - step, step)  # time axis in seconds

    # Step 5: Print energy and pitch (spectral centroid) values and check for deviations
    print("Timestamps, Energy, Spectral Centroid (Pitch) values:")
    for i in range(len(energy)):
        # Get the timestamp in seconds
        timestamp = time[i]

        # Print the energy and pitch values at this timestamp
        print(f"{timestamp:.2f}s - Energy: {energy[i]:.3f}, Spectral Centroid (Pitch): {spectral_centroid[i]:.3f}")

        # Check if either energy or spectral centroid exceeds the threshold
        if energy[i] > energy_threshold or spectral_centroid[i] > pitch_threshold:
            timestamps.append(timestamp)

    return timestamps


# Example Usage

# Step 1: Convert MP3 to WAV

# Step 2: Detect deviations in the WAV file


def interact_with_agent(audio_file):
    convert_mp3_to_wav(audio_file, wav_file)
    deviations = detect_deviations(pitch_threshold=0.15, energy_threshold=0.2, window_size=1.0, step_size=0.5)
    # Step 3: Output detected deviations

    if not deviations:
        print("No significant deviations detected.")
        deviations = []
    return [f"{timestamp:.2f}s" for timestamp in deviations]

if __name__ == '__main__':
    print(interact_with_agent(mp3_file))
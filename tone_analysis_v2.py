from pyAudioAnalysis import ShortTermFeatures as aF
from pyAudioAnalysis import audioBasicIO as aIO
from pydub import AudioSegment
import numpy as np


def convert_mp3_to_wav(mp3_file, wav_file):
    """
    Converts an MP3 file to WAV format using pydub.
    """
    audio = AudioSegment.from_mp3(mp3_file)
    audio = audio.set_channels(1)
    audio.export(wav_file, format="wav")
    print(f"Conversion complete! WAV file saved as: {wav_file}")


def detect_deviations(audio_file, window_size=1.0, step_size=0.5, std_multiplier=2):
    """
    Analyzes the audio file for deviations in multiple features linked to anger/frustration.

    Args:
    - audio_file: Path to the WAV file.
    - window_size: Window size for feature extraction (seconds).
    - step_size: Step size for feature extraction (seconds).
    - std_multiplier: Multiplier for standard deviation to set adaptive thresholds.

    Returns:
    - A list of time intervals (timestamps) where significant deviations occur.
    """
    # Step 1: Read audio data from the file
    fs, s = aIO.read_audio_file(audio_file)

    # Step 2: Extract short-term features
    win, step = window_size, step_size
    features, feature_names = aF.feature_extraction(s, fs, int(fs * win), int(fs * step))

    # Step 3: Identify indices of relevant features
    feature_indices = {
        "energy": feature_names.index('energy'),
        "energy_entropy": feature_names.index('energy_entropy'),
        "spectral_spread": feature_names.index('spectral_spread'),
        "spectral_flux": feature_names.index('spectral_flux'),
        "mfcc_1": feature_names.index('mfcc_1'),
        "delta_mfcc_1": feature_names.index('delta mfcc_1'),
    }

    # Extract values for selected features
    energy = features[feature_indices["energy"], :]
    energy_entropy = features[feature_indices["energy_entropy"], :]
    spectral_spread = features[feature_indices["spectral_spread"], :]
    spectral_flux = features[feature_indices["spectral_flux"], :]
    mfcc_1 = features[feature_indices["mfcc_1"], :]
    delta_mfcc_1 = features[feature_indices["delta_mfcc_1"], :]

    # Calculate adaptive thresholds based on mean + std deviation
    thresholds = {
        "energy": np.mean(energy) + std_multiplier * np.std(energy),
        "energy_entropy": np.mean(energy_entropy) + std_multiplier * np.std(energy_entropy),
        "spectral_spread": np.mean(spectral_spread) + std_multiplier * np.std(spectral_spread),
        "spectral_flux": np.mean(spectral_flux) + std_multiplier * np.std(spectral_flux),
        "mfcc_1": np.mean(mfcc_1) + std_multiplier * np.std(mfcc_1),
        "delta_mfcc_1": np.mean(delta_mfcc_1) + std_multiplier * np.std(delta_mfcc_1),
    }

    # Step 4: Detect deviations based on computed thresholds
    timestamps = []
    duration = len(s) / float(fs)  # in seconds
    time = np.arange(0, duration - step, step)  # time axis in seconds

    print("Timestamps, Energy, Spectral Spread, Spectral Flux, MFCC 1, ΔMFCC 1:")

    for i in range(len(energy)):
        timestamp = time[i]

        # Log feature values
        print(f"{timestamp:.2f}s - Energy: {energy[i]:.3f}, "
              f"Spectral Spread: {spectral_spread[i]:.3f}, "
              f"Spectral Flux: {spectral_flux[i]:.3f}, "
              f"MFCC_1: {mfcc_1[i]:.3f}, ΔMFCC_1: {delta_mfcc_1[i]:.3f}")

        # Check if any feature exceeds its adaptive threshold
        if (energy[i] > thresholds["energy"] or
                energy_entropy[i] > thresholds["energy_entropy"] or
                spectral_spread[i] > thresholds["spectral_spread"] or
                spectral_flux[i] > thresholds["spectral_flux"] or
                mfcc_1[i] > thresholds["mfcc_1"] or
                delta_mfcc_1[i] > thresholds["delta_mfcc_1"]):
            timestamps.append(timestamp)

    return timestamps


# Example Usage
mp3_file = "/Users/parag/Downloads/every_tech_support_call_ever.mp3"
wav_file = "customer_call.wav"

# Step 1: Convert MP3 to WAV
convert_mp3_to_wav(mp3_file, wav_file)

# Step 2: Detect deviations in the WAV file
deviations = detect_deviations(wav_file, window_size=1.0, step_size=0.5, std_multiplier=2)

# Step 3: Output detected deviations
if deviations:
    print(f"Deviations detected at the following timestamps (in seconds):")
    for timestamp in deviations:
        print(f"{timestamp:.2f}s")
else:
    print("No significant deviations detected.")

import torch
import torchaudio
import odas_wrapper as odas
from train_model import AudioModel
import numpy as np
from triangulate import triangulate

# Load the trained model
model = AudioModel()
model.load_state_dict(torch.load("drone_sound_model.pth"))
model.eval()

# Load an audio file
audio_path = "drone_sounds/drone_audio.wav"
audio, sample_rate = torchaudio.load(audio_path)

# Preprocess the audio and convert to a Mel spectrogram
audio = torch.mean(audio, axis=0)
resample = torchaudio.transforms.Resample(sample_rate, 32000)
audio = resample(audio)
num_samples = 32000 * 5
if audio.shape[0] > num_samples:
    audio = audio[:num_samples]
elif audio.shape[0] < num_samples:
    audio = torch.nn.functional.pad(audio, (0, num_samples - audio.shape[0]))
melspectrogram = torchaudio.transforms.MelSpectrogram(sample_rate=32000, n_mels=128)
melspec = melspectrogram(audio)

# Make a prediction
with torch.no_grad():
    prediction = model(melspec.unsqueeze(0).unsqueeze(0))

# If a drone is detected, pass the audio to ODAS
if prediction.item() > 0.5:
    print("Drone detected! Passing audio to ODAS for processing.")

    # Create a dummy msg_spectra_obj for demonstration
    cfg = odas.MsgSpectraCfg(halfFrameSize=1024, nChannels=1, fS=32000)
    msg = odas.msg_spectra_construct(odas.ctypes.pointer(cfg))

    # In a real application, you would populate the msg object with the actual audio data from multiple microphones.
    # For now, we'll just print a message.
    print("ODAS message created. In a real application, this would be passed to the ODAS processing pipeline.")

    # In a real application, you would get the sound source directions from the ODAS library.
    # For now, we'll use dummy data.
    mic_positions = [
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 0),
        (1, 1, 0)
    ]
    source_directions = [
        (1, 1, 1),
        (0, 1, 1),
        (1, 0, 1),
        (0, 0, 1)
    ]

    estimated_position = triangulate(mic_positions, source_directions)
    print(f"Estimated position: {estimated_position}")


    odas.msg_spectra_destroy(msg)
else:
    print("No drone detected.")

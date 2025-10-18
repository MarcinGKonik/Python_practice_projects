import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchaudio
import torchaudio.transforms as T
import timm
import os
import pandas as pd
from pytubefix import YouTube
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


# Download audio from YouTube
def download_drone_audio(url, output_path="drone_sounds"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=output_path, filename="drone_audio.mp4")

    # Convert to wav
    os.system(f"ffmpeg -i {output_path}/drone_audio.mp4 {output_path}/drone_audio.wav")

    return f"{output_path}/drone_audio.wav"

class AudioDataset(Dataset):
    def __init__(self, df, target_sample_rate=32000, audio_length=5):
        self.df = df
        self.file_paths = df['file_path'].values
        self.labels = df['label'].values
        self.target_sample_rate = target_sample_rate
        self.num_samples = target_sample_rate * audio_length

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        # Load audio from file to waveform
        audio, sample_rate = torchaudio.load(self.file_paths[index])

        # Convert to mono
        audio = torch.mean(audio, axis=0)

        # Resample
        if sample_rate != self.target_sample_rate:
            resample = T.Resample(sample_rate, self.target_sample_rate)
            audio = resample(audio)

        # Adjust number of samples
        if audio.shape[0] > self.num_samples:
            audio = audio[:self.num_samples]
        elif audio.shape[0] < self.num_samples:
            audio = torch.nn.functional.pad(audio, (0, self.num_samples - audio.shape[0]))

        # Convert to Mel spectrogram
        melspectrogram = T.MelSpectrogram(sample_rate=self.target_sample_rate, n_mels=128)
        melspec = melspectrogram(audio)

        return {"image": melspec.unsqueeze(0), "label": torch.tensor(self.labels[index]).float()}

class AudioModel(nn.Module):
    def __init__(self, model_name='tf_efficientnet_b0_ns', pretrained=True, num_classes=1):
        super(AudioModel, self).__init__()
        self.model = timm.create_model(model_name, pretrained=pretrained, in_chans=1)
        self.in_features = self.model.classifier.in_features
        self.model.classifier = nn.Sequential(
            nn.Linear(self.in_features, num_classes),
            nn.Sigmoid()
        )

    def forward(self, images):
        logits = self.model(images)
        return logits


if __name__ == "__main__":
    # Download audio and create dataset
    audio_path = download_drone_audio("https://www.youtube.com/watch?v=ctEksNz7tqg")
    data = {'file_path': [audio_path], 'label': [1]}
    df = pd.DataFrame(data)

    # Create dataset and dataloader
    dataset = AudioDataset(df)
    dataloader = DataLoader(dataset, batch_size=1)

    # Create model, loss function, and optimizer
    model = AudioModel()
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    num_epochs = 3
    for epoch in range(num_epochs):
        for batch in dataloader:
            images = batch['image']
            labels = torch.ones(1)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs.squeeze(1), labels)
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}")

    # Save the model
    torch.save(model.state_dict(), "drone_sound_model.pth")

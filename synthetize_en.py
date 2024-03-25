import torch
from scipy.io.wavfile import write

from tacotron2.hparams import create_hparams
from tacotron2.model import Tacotron2
from tacotron2.text import text_to_sequence
from waveglow.glow import WaveGlow

if torch.cuda.is_available():
    device = "cuda:0"
    devname = torch.cuda.get_device_name(device)
    print(f"Using device {devname}.")
else:
    device = "cpu"
    print("Using cpu.")

# General configuration
n_mel_channels = 80

# Tacotron2 configuration
sampling_rate = 22050
max_decoder_steps = 5000
gate_threshold = 0.1

# WaveGlow configuration
n_mel_channels: 80
n_flows = 12
n_group = 8
n_early_every = 4
n_early_size = 2
WN_config = {
    "n_layers": 8,
    "n_channels": 512,
    "kernel_size": 3,
}
sigma = 1.0


# Tacotron2 parameters
hparams = create_hparams()
hparams.sampling_rate = sampling_rate
hparams.max_decoder_steps = max_decoder_steps
hparams.gate_threshold = gate_threshold
hparams.n_mel_channels = n_mel_channels

# Load Tacotron2
tacotron2 = Tacotron2(hparams)
tacotron2.load_state_dict(torch.load("models/tacotron2_en.pth"))
tacotron2.to(device)

# Load WaveGlow
waveglow = WaveGlow(
    n_mel_channels,
    n_flows,
    n_group,
    n_early_every,
    n_early_size,
    WN_config,
)

waveglow.load_state_dict(torch.load("models/waveglow_en.pth"))
waveglow = waveglow.remove_weightnorm(waveglow)
waveglow = waveglow.to(device)

# Evaluation mode
tacotron2.eval()
waveglow.eval()

text = "Hello world, I missed you so much. The world is beautifull."
sequences = torch.LongTensor(
    text_to_sequence(text, ['english_cleaners'])
).unsqueeze(dim=0).to(device)

with torch.no_grad():
    _, mel_postnet, _, _ = tacotron2.inference(sequences)
    audio = waveglow.infer(mel_postnet, sigma)
audio_numpy = audio[0].data.cpu().numpy()

write("speech.wav", sampling_rate, audio_numpy)

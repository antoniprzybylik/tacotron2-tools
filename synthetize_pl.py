import torch
from scipy.io.wavfile import write

from tacotron2.hparams import create_hparams
from tacotron2.model import Tacotron2
from tacotron2.mekatron2_text_pl import text_to_sequence
from waveglow.glow import WaveGlow
from waveglow.denoiser import Denoiser

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
gate_threshold = 0.001
n_symbols = 155

# WaveGlow configuration
n_mel_channels: 80
n_flows = 12
n_group = 8
n_early_every = 4
n_early_size = 2
WN_config = {
    "n_layers": 8,
    "n_channels": 256,
    "kernel_size": 3,
}
sigma = 1.0

# Denoiser configuration
denoise_strength = 0.06


# Tacotron2 parameters
hparams = create_hparams()
hparams.sampling_rate = sampling_rate
hparams.max_decoder_steps = max_decoder_steps
hparams.gate_threshold = gate_threshold
hparams.n_mel_channels = n_mel_channels
hparams.n_symbols = 155

# Load Tacotron2
tacotron2 = Tacotron2(hparams)
tacotron2.load_state_dict(torch.load("models/tacotron2_shepard_pl.pth"))
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

waveglow.load_state_dict(torch.load("models/waveglow_shepard_pl.pth"))
waveglow = waveglow.remove_weightnorm(waveglow)
waveglow = waveglow.to(device)

# Evaluation mode
tacotron2.eval()
waveglow.eval()

# Denoiser
denoiser = Denoiser(waveglow)

text = "Ala ma kota, a kot ma alę."
sequences = torch.LongTensor(
    text_to_sequence(text, ['basic_cleaners'])
).unsqueeze(dim=0).to(device)

with torch.no_grad():
    _, mel_postnet, _, _ = tacotron2.inference(sequences)
    audio = waveglow.infer(mel_postnet, sigma)
    denoised_audio = denoiser(audio, strength=denoise_strength)[:, 0]
audio_numpy = audio[0].data.cpu().numpy()

write("speech.wav", sampling_rate, audio_numpy)

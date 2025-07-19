from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import soundfile as sf

def transcribe_audio_hindi(audio_path):
    try:
        print("📝 Loading Hindi transcription model...")
        processor = Wav2Vec2Processor.from_pretrained("Harveenchadha/vakyansh-wav2vec2-hindi-him-4200")
        model = Wav2Vec2ForCTC.from_pretrained("Harveenchadha/vakyansh-wav2vec2-hindi-him-4200")

        # Load audio and resample to 16kHz
        speech, original_rate = sf.read(audio_path)
        if original_rate != 16000:
            import torchaudio
            import torchaudio.transforms as T
            # Convert stereo to mono
            if speech.ndim > 1:
                speech = speech.mean(axis=1)
            resampler = T.Resample(orig_freq=original_rate, new_freq=16000)
            speech_tensor = torch.tensor(speech).unsqueeze(0)
            speech_16k = resampler(speech_tensor).squeeze().numpy()
        else:
            speech_16k = speech

        # Process with the model
        input_values = processor(speech_16k, sampling_rate=16000, return_tensors="pt", padding=True).input_values

        print("🎤 Transcribing audio (Hindi)...")
        with torch.no_grad():
            logits = model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)[0]
        return transcription
    except Exception as e:
        print(f"Error during Hindi transcription: {e}")
        return None

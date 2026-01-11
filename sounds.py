import math
import struct
try:
    import simpleaudio as sa
except Exception:
    sa = None

def _generate_tone(frequency=440.0, duration=0.25, volume=0.5, sample_rate=44100):
    n_samples = int(sample_rate * duration)
    buf = bytearray()
    max_amp = int(32767 * volume)
    for i in range(n_samples):
        t = i / sample_rate
        val = int(max_amp * math.sin(2 * math.pi * frequency * t))
        buf += struct.pack('<h', val)
    return bytes(buf), sample_rate

class SoundManager:
    def __init__(self):
        self.available = sa is not None

    def play_finish(self):
        """Play a short finish tone."""
        if not self.available:
            print("SOUND: finish")
            return
        samples, sr = _generate_tone(frequency=880.0, duration=0.25, volume=0.8)
        try:
            sa.play_buffer(samples, 1, 2, sr)
        except Exception:
            pass

    def play_haptic_beep(self):
        """Short low beep used as haptic fallback."""
        if not self.available:
            print("SOUND: haptic")
            return
        samples, sr = _generate_tone(frequency=150.0, duration=0.06, volume=0.5)
        try:
            sa.play_buffer(samples, 1, 2, sr)
        except Exception:
            pass

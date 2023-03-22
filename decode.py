import pyaudio
import numpy as np

# DTMF frequencies
tones = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477)
}

# Callback function for audio stream
def callback(in_data, frame_count, time_info, status):
    audio_data = np.fromstring(in_data, dtype=np.int16)
    freq_data = np.fft.fft(audio_data)
    freq_data = np.abs(freq_data[0:len(freq_data)//2])
    max_freq = np.argmax(freq_data)
    freq = max_freq * fs / len(freq_data)
    for key in tones:
        if abs(freq - tones[key][0]) < 20 and abs(freq - tones[key][1]) < 20:
            print(key, end='', flush=True)
            break
    return (in_data, pyaudio.paContinue)

# Open audio stream
p = pyaudio.PyAudio()
fs = 44100
stream = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024, stream_callback=callback)

# Start audio stream
stream.start_stream()

# Wait for stream to finish
while stream.is_active():
    pass

# Stop audio stream
stream.stop_stream()
stream.close()
p.terminate()

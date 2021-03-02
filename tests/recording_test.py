import alsaaudio as audio
import wave
import time

device = 'default'

SOUNDS_DIR = '../sounds/'
file = open(SOUNDS_DIR + 'recording.wav', 'wb')


p = audio.PCM(audio.PCM_CAPTURE,audio.PCM_NONBLOCK, channels=2, rate=44100,
		format=audio.PCM_FORMAT_S16_LE, periodsize=160, device=device) 

t_end = time.time() + 5
while (time.time() < t_end):
	l, data = p.read()
	if l:
		file.write(data)
		time.sleep(.001)

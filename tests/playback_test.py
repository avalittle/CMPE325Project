import alsaaudio
import wave

print(alsaaudio.pcms())
print(alsaaudio.cards())

SOUNDS_DIR = '../sounds/'
p = alsaaudio.PCM(cardindex=1, rate=96000)
file = wave.open(SOUNDS_DIR + 'recording.wav', 'rb')
data = file.readframes(1024)

while data:
	p.write(data)
	data = file.readframes(1024)


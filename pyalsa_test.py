import alsaaudio
import wave

print(alsaaudio.pcms())
print(alsaaudio.cards())

p = alsaaudio.PCM(cardindex=1, rate=96000)
file = wave.open('saved_sounds/ava.wav', 'rb')
data = file.readframes(1024)

while data:
	p.write(data)
	data = file.readframes(1024)


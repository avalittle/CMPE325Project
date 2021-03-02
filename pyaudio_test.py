import pyaudio
import wave
filename = 'saved_sounds/ava.wav'

chunk = 1024
wf = wave.open(filename, 'rb')

p = pyaudio.PyAudio()

info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
print(numdevices)
for i in range(0, numdevices):
	if (p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')) > 0:
		print("Input device id",i," - " ,p.get_device_info_by_host_api_device_index(0,i).get('name'))


stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), output_device_index=1, channels = wf.getnchannels(), 
	rate = wf.getframerate(),output=True)

data = wf.readframes(chunk)
while data != '':
	stream.write(data)
	data = wf.readframes(chunk)

stream.close()
p.terminate()

# Flask Imports
from flask import Flask
from flask import request
from flask import jsonify

# PyAudio Imports
import alsaaudio
import pyaudio
import wave

import json

app = Flask(__name__)
# End point for recording audio of child
@app.route('/recording', methods = ['GET'])
def recording(length):
	capture_recording(length)
	return "recording"

# Functionality for recording audio
def capture_recording(length):
	form_1 = pyaudio.paInt16 # 16-bit resolution
	chans = 1 # 1 channel
	samp_rate = 44100 # 44.1kHz sampling rate
	chunk = 4096 # 2^12 samples for buffer
	dev_index = 2 # device index found by p.get_device_info_by_index(ii)
	wav_output_filename = 'output.wav' # name of .wav file

	audio = pyaudio.PyAudio() # create pyaudio instantiation

	# create pyaudio stream
	stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
	print("recording")
	frames = []

	# loop through stream and append audio chunks to frame array
	for ii in range(0,int((samp_rate/chunk)*length)):
		data = stream.read(chunk)
		frames.append(data)

	print("finished recording")

	# stop the stream, close it, and terminate the pyaudio instantiation
	stream.stop_stream()
	stream.close()
	audio.terminate()

	# save the audio frames as .wav file
	wavefile = wave.open(wav_output_filename,'wb')
	wavefile.setnchannels(chans)
	wavefile.setsampwidth(audio.get_sample_size(form_1))
	wavefile.setframerate(samp_rate)
	wavefile.writeframes(b''.join(frames))
	wavefile.close()



@app.route ('/playback', methods = ['POST'])
def playback():
	print ("Playback baby!")
	return "playback"

# Endpoint for playing sound on bear
@app.route('/playback/<audio_file>', methods = ['POST'])
def playbackSpecific(audio_file):
	print("Playing a specific audio recording %s" % str(audio_file))
	playback_recording(audio_file)
	return "Played recording!"

# Returns list of available audio sounds to play on bear (saved sounds)
@app.route('/playback', methods = ['GET'])
def getAllPlaybacks():
	return json.dumps(['ava1', 'ava2'])

# Functionality for playing sound on bear
def playback_recording(audio_file):
	p = alsaaudio.PCM(cardindex=1)
	p.setrate(96000)
	file = wave.open('saved_sounds/' + str(audio_file), 'rb')
	data = file.readframes(1024)

	while data:
		p.write(data)
		data = file.readframes(1024)

if __name__ == '__main__':
	app.run(debug=True, port=80, host='0.0.0.0')

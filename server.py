# Flask Imports
from flask import Flask
from flask import request
from flask import jsonify

# PyAudio Imports
import alsaaudio
import wave

import json

app = Flask(__name__)
@app.route('/recording', methods = ['GET', 'POST'])
def recording():
	if request.method == 'POST':
		print ("Recording post")
	else: 
		print ("Recording GET")
	return "recording"

@app.route ('/playback', methods = ['POST'])
def playback():
	print ("Playback baby!")
	return "playback"

@app.route('/playback/<audio_file>', methods = ['POST'])
def playbackSpecific(audio_file):
	print("Playing a specific audio recording %s" % str(audio_file))
	playback_recording(audio_file)
	return "Played recording!"

@app.route('/playback', methods = ['GET'])
def getAllPlaybacks():
	return json.dumps(['ava1', 'ava2'])


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

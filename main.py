#!/usr/bin/python
import os
from os import listdir
from os.path import isfile, join

import time
# Flask Imports
from flask import Flask
from flask import request
from flask import jsonify
from flask import send_file, send_from_directory

# Custom Imports
from api import success, error
from files import save_file, delete_file
from audio import do_recording, playback_recording, change_volume

app = Flask(__name__)
################################################################################
################################  Recording  ###################################
################################################################################

# Works on Pi
@app.route('/recording', methods=['GET'])
def get_recording():
    print ('Getting a voice recording from the server!')

    length = request.args.get('length')
    if length is None:
        length = 10

    if int(length) < 0:
        return error(400, 'Validation Error',
                     'Recording length must be greater than 0!')
    try:
        do_recording(int(length))
	time.sleep(int(length))
        return send_from_directory('sounds/',
                                   filename='captured_recording.wav',
                                   as_attachment=True)
    except Exception as e:
        return error(500, 'Internal Server Error', str(e))


    return success(200, 'Recorded succesfully!')

# Makes bear talk but doesn't save file
@app.route('/recording', methods=['POST'])
def post_recording():

	if 'file' not in request.files:
		return error(400, 'Validation Error', 'You must supply a file!')
	if 'fileName' not in request.form: 
		return error(400, 'Validation Error', 'You must supply a file name')

	file_name = request.form['fileName']
	file = request.files['file']
	try:
		save_file(str(file_name), file)
	except Exception as e:
        	return error(500, 'Internal Server Error', str(e))

	return success(200, 'Recording saved succesfully!')

################################################################################
################################  Playback  ####################################
################################################################################
# Returns list of available audio sounds to play on bear (saved sounds)

# Works on Pi. Not using display name
@app.route('/playback', methods=['GET'])
def getAllPlaybacks():
    # items = { 
    #     'items': [
    #         { 
    #             'displayName': 'Ava Is the best girlfriend ever!!!!',
    #             'fileName': 'ava.wav'
    #         },
    #         { 
    #             'displayName': 'WOOOOOO',
    #             'fileName': 'test.wav'
    #         },
    #     ]
    #  } 
    files = [f for f in listdir('sounds/') if isfile (join('sounds/', f))]
    files = {'files': files}

    return success(200, 'Succesfully retrieved audio files!', files)

# Works on Pi. 
@app.route('/playback', methods=['PUT'])
def playback():
	msg = 'Request to upload file received'
	print(request.files)

	# Validate file
	if 'file' not in request.files:
		return error(400, 'Validation Error', 'You must supply a file')

	# Validate display name
	if 'displayName' not in request.form:
		return error(400, 'Validation Error', 'You must supply a display name')

	if 'fileName' not in request.form:
		return error(400, 'Validation Error', 'You must supply a file name')

	display_name = request.form['displayName']
	file_name = request.form['fileName']
	file = request.files['file']

	try:
		save_file(str(file_name), file)
		playback_recording(file_name)
		delete_file('sounds/' + str(file_name))
	except Exception as e:
		return error(500, 'Internal Server Error', str(e))

	return success(200, msg)

# Endpoint for playing sound on bear

# Works on Pi. 
@app.route('/playback/<file>', methods=['POST'])
def playbackFile(file):
    msg = 'Playing a specific audio recording %s' % str(file)
    print(msg)
    #if 'fileName' not in request.form: 
        #return error(400, 'Validation Error', 'You must supply a file name')
	
    #file = request.form['fileName']
    try: 
        playback_recording(file)
    except Exception as e:
        return error(500, 'Internal Server Error', str(e))

    return success(200, msg)

# Works on Pi
@app.route('/playback/<file>', methods=['DELETE'])
def deletePlayback(file):
    msg = 'Request to delete file %s received' % file
    print(msg)
    
    if not os.path.exists('sounds/' + str(file)):
        return success(204, msg)
    else:
        delete_file('sounds/' + str(file))
        return success(200, msg)


################################################################################
################################  Volume  ######################################
################################################################################

@app.route('/volume', methods=['POST'])
def volume():
	msg = 'Changing volume on teddbyear'
 	print(msg)
	change_in_vol = request.args.get('changeInVolume')
	if change_in_vol is None:
		change_in_vol = 0
	try:
		change_volume(int(change_in_vol))
	except Exception as e:
		return error(500, 'Internal Server Error', str(e))
	return success(200, msg)

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')

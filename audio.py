# PyAudio Imports
import alsaaudio
# import pyaudio
import wave
import sys
import os
import getopt

def do_recording(time):
    print("Doing recording")

    out_file = 'sounds/captured_recording.wav'
    opts, args = getopt.getopt(sys.argv[1:], 'd:')
    for o, a in opts: 
        if o == '-f':
            out_file = a
        if o == '-l':
            time = a
    os.system('arecord -f S16_LE -c 2 -r 96000 -d ' + str(time) + ' ' + out_file)

def playback_recording(filepath):
    print("Playing recording")
    print(filepath)
    p = alsaaudio.PCM(cardindex=1)
    p.setrate(96000)
    file = wave.open('sounds/' + str(filepath), 'rb')
    data = file.readframes(1024)
    
    while data:
        p.write(data)
        data = file.readframes(1024)

def change_volume(number):
	m = alsaaudio.Mixer(cardindex=1)
	vol = m.getvolume()
	vol = int(vol[0])
	m.setvolume(number+vol) 
	print("Changing volume")




# # Functionality for recording audio
# def capture_recording(length):
# 	form_1 = pyaudio.paInt16 # 16-bit resolution
# 	chans = 1 # 1 channel
# 	samp_rate = 44100 # 44.1kHz sampling rate
# 	chunk = 4096 # 2^12 samples for buffer
# 	dev_index = 2 # device index found by p.get_device_info_by_index(ii)
# 	wav_output_filename = 'output.wav' # name of .wav file
# 	path_to_file = "/output.wav"

# 	audio = pyaudio.PyAudio() # create pyaudio instantiation

# 	# create pyaudio stream
# 	stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
#                     input_device_index = dev_index,input = True, \
#                     frames_per_buffer=chunk)
# 	print("recording")
# 	frames = []

# 	# loop through stream and append audio chunks to frame array
# 	for ii in range(0,int((samp_rate/chunk)*length)):
# 		data = stream.read(chunk)
# 		frames.append(data)

# 	print("finished recording")

# 	# stop the stream, close it, and terminate the pyaudio instantiation
# 	stream.stop_stream()
# 	stream.close()
# 	audio.terminate()

# 	# save the audio frames as .wav file
# 	wavefile = wave.open(wav_output_filename,'wb')
# 	wavefile.setnchannels(chans)
# 	wavefile.setsampwidth(audio.get_sample_size(form_1))
# 	wavefile.setframerate(samp_rate)
# 	wavefile.writeframes(b''.join(frames))
# 	wavefile.close()

# 	return send_file(path_to_file, mimetype="audio/wav",as_attachment=True, attachment_filename="output.wav")

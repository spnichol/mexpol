# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 17:35:01 2017
#!/usr/bin/python
@author: spnichol
"""
import base64
import sox 
direc = "test/amlo_hmm/"
wav_file = "amlo_mix.wav"
new_file = direc+wav_file+".flac"

def to_flac(direc, wav_file):
        command="ffmpeg -i " +direc+wav_file+ " -acodec flac -bits_per_raw_sample 16 -ar 16000 -ac 1 "+direc+wav_file+".flac"
        #command = "ffmpeg -i " +direc+wav_file+ " -c:a flac "+direc+wav_file+".flac"
        new_file = direc+wav_file+".flac"
        subprocess.call(command, shell=True)
        return direc, wav_file 


to_flac(direc, wav_file)

with open(direc+wav_file+".flac", 'rb') as speech:
    # Base64 encode the binary audio file for inclusion in the JSON
    # request.
    speech_content = base64.b64encode(speech.read())


from google.cloud import speech
client = speech.Client()
with open("test/amlo_hmm/audio.flac", 'rb') as f:
    audio = client.sample(f.read(), sample_rate=16000, encoding='FLAC')
    results = audio.sync_recognize(language_code="es-MX", max_alternatives=2)
    for result in results:
        for alternative in result.alternatives:
            print alternative.transcript
            print alternative.confidence
        

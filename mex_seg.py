# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 13:35:31 2017

@author: spnichol
"""

from pyAudioAnalysis import audioSegmentation as aS
from audioSegmentation import speakerDiarization
from audioSegmentation import silenceRemoval

from pyAudioAnalysis import audioTrainTest as aT
#print aT.featureAndTrain(["amlo/","not_amlo/", "music/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "data/newmusamlo_svm")

#knn with short term window and short term step 
#aT.featureAndTrain(["amlo/","not_amlo/", "music/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "knndiffparam")
#print aT.featureAndTrain(["amlo/","not_amlo/", "music/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "extratrees", "data/amlo_extra")

#
#aT.featureAndTrain(["/home/tyiannak/Desktop/MusicGenre/Classical/","/home/tyiannak/Desktop/MusicGenre/Electronic/","/home/tyiannak/Desktop/MusicGenre/Jazz/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "extratrees", "etMusicGenre3", True)
#aT.featureAndTrain(["/home/tyiannak/Desktop/MusicGenre/Classical/","/home/tyiannak/Desktop/MusicGenre/Electronic/","/home/tyiannak/Desktop/MusicGenre/Jazz/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "gradientboosting", "gbMusicGenre3", True)
#aT.featureAndTrain(["/home/tyiannak/Desktop/MusicGenre/Classical/","/home/tyiannak/Desktop/MusicGenre/Electronic/","/home/tyiannak/Desktop/MusicGenre/Jazz/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "randomforest", "rfMusicGenre3", True)
#aT.featureAndTrain(["/home/tyiannak/Desktop/5Class/Silence/","/home/tyiannak/Desktop/5Class/SpeechMale/","/home/tyiannak/Desktop/5Class/SpeechFemale/","/home/tyiannak/Desktop/5Class/ObjectsOther/","/home/tyiannak/Desktop/5Class/Music/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "svm5Classes")
#aT.featureAndTrain(["/home/tyiannak/Desktop/5Class/Silence/","/home/tyiannak/Desktop/5Class/SpeechMale/","/home/tyiannak/Desktop/5Class/SpeechFemale/","/home/tyiannak/Desktop/5Class/ObjectsOther/","/home/tyiannak/Desktop/5Class/Music/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "knn5Classes")
#aT.featureAndTrain(["/home/tyiannak/Desktop/5Class/Silence/","/home/tyiannak/Desktop/5Class/SpeechMale/","/home/tyiannak/Desktop/5Class/SpeechFemale/","/home/tyiannak/Desktop/5Class/ObjectsOther/","/home/tyiannak/Desktop/5Class/Music/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "extratrees", "et5Classes")
#aT.featureAndTrain(["/home/tyiannak/Desktop/5Class/Silence/","/home/tyiannak/Desktop/5Class/SpeechMale/","/home/tyiannak/Desktop/5Class/SpeechFemale/","/home/tyiannak/Desktop/5Class/ObjectsOther/","/home/tyiannak/Desktop/5Class/Music/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "gradientboosting", "gb5Classes")
#aT.featureAndTrain(["/home/tyiannak/Desktop/5Class/Silence/","/home/tyiannak/Desktop/5Class/SpeechMale/","/home/tyiannak/Desktop/5Class/SpeechFemale/","/home/tyiannak/Desktop/5Class/ObjectsOther/","/home/tyiannak/Desktop/5Class/Music/"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "randomforest", "rf5Classes")
#


#classify as amlo or not 
#flagsInd, classesAll, acc, CM] = aS.mtFileClassification("test/amlo_mix3.wav", "data/newamlo_svm", "svm", True)

#try with adding music 
#[flagsInd, classesAll, acc, CM] = aS.mtFileClassification("test/amlo_mix4.wav", "data/musamlo_svm", "svm", True)


#try with knn and short term window and short term step 
#[flagsInd, classesAll, acc, CM] = aS.mtFileClassification("test/amlo_mix4.wav", "knndiffparam", "knn", True)

#[flagsInd, classesAll, acc, CM] = aS.mtFileClassification("test/amlo_mix4.wav", "data/amlo_forest", "randomforest", True)
#flagsInd, classesAll, acc, CM] = aS.mtFileClassification("test/amlo_mix3.wav", "data/amlo_extra", "extratrees", True)

#speakerDiarization("amlo/amlo3.wav", 2)

#Silence removal 
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
import re
import soundfile as sf

import subprocess
import os 
##python audioAnalysis.py silenceRemoval -i test/amlo_mix.wav --smoothing 0.7 --weight 0.9
# #
direc="test/"
wav_file = "amlo_mix4.wav"

[Fs, x] = aIO.readAudioFile(direc+wav_file)
segments = aS.silenceRemoval(x, Fs, 0.020, 0.020, smoothWindow =.7, Weight = .9, plot = True)
newpath = direc+wav_file+"segs"
original = direc+wav_file
f = sf.SoundFile(direc+wav_file)
frames = len(f)
sample_rate =float(f.samplerate)
print(sample_rate)

time = frames/float(sample_rate)
print time

#
#
#
#if not os.path.exists(newpath):
#    os.makedirs(newpath)
#
#for seg in segments: 
#    beg = str(round(seg[0], 2))
#    end = str(round(seg[1], 2))
#    command = "ffmpeg -i "+original+ " -c copy -map " + beg + " -segment_time " + end + " -f segment " +newpath+"output%03d.wav"
#    subprocess.call(command, shell=True)
#

#remove_Silence("test/", "amlo_mix3.wav")


#[Fs, x] = aIO.readAudioFile("test/amlo_mix3.wav")
#diar = aS.speakerDiarization(x, 2, PLOT=True)
#


#python audioAnalysis.py silenceRemoval -i test/amlo_mix4.wav --smoothing 0.8 --weight 0.2
#python audioAnalysis.py classifyFolder -i test/amlo_mix4.wav --model svm --classifier data/musamlo_svm --detail
#try HMM
#command = "ffmpeg -i test/amlo_mix.wav -c copy -map + 0  -segment_time  30.06 -f segment test_one.wav"
#subprocess.call(command, shell=True)

from pyAudioAnalysis import audioSegmentation as aS
#aS.trainHMM_fromFile('output2.wav', 'test/amlo_mix.segments', 'hmmTemp4', 1.0, 1.0)



#aS.hmmSegmentation('output2.wav', 'hmmTemp4', True, 'test/amlo_mix.segments')             # test 1
#aS.hmmSegmentation('data/scottish.wav', 'hmmTemp2', True, 'data/scottish.segments')             # test 2

#python audioAnalysis.py trainHMMsegmenter_fromfile -i test/amlo_mix.wav --ground test/amlo_mix.segments -o hmmcount -mw 0.1 -ms 0.1   

#try feature extraction 
#from pyAudioAnalysis import audioBasicIO
#from pyAudioAnalysis import audioFeatureExtraction
#import matplotlib.pyplot as plt
#[Fs, x] = audioBasicIO.readAudioFile("output2.wav");
#F = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.050*Fs, 0.025*Fs);
#plt.subplot(2,1,1); plt.plot(F[0,:]); plt.xlabel('Frame no'); plt.ylabel('ZCR'); 
#plt.subplot(2,1,2); plt.plot(F[1,:]); plt.xlabel('Frame no'); plt.ylabel('Energy'); plt.show()

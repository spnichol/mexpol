# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:28:43 2017

@author: spnichol
"""

#resampling 
import csv
import pandas as pd
from numpy import nan
import subprocess
from subprocess import call 
import re
import soundfile as sf
from os import listdir
from os.path import isfile, join
import wave
from pyAudioAnalysis import audioSegmentation as aS
from pyAudioAnalysis import audioTrainTest as aT
import numpy 

#convert to 16000

def conv_samp(direc, wav_file):
    command = "ffmpeg -i " +direc+"/"+wav_file+ " -ac 1 -ab 44100 -ar 16000 " + direc+ wav_file +".wav" + " -y"
    subprocess.call(command, shell=True)

def trainSVM():
    aT.featureAndTrain(["amlo/","not_amlo"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "svm_amlo_v1")    


def train():
    #train on several files 

    aS.trainHMM_fromDir('test/amlo_hmm/', 'amlo_hmm', 1.0, 1.0) 

    ##try model with shorter mid-term windows

    aS.trainHMM_fromDir('test/amlo_hmm/', 'amlo_hmm_short', 0.1, 0.1) 

def aud_classify(direc, wav_file):
##test on one file                          
    global j
    global l
    print "classifying" + direc+wav_file
    [flagsInd, classesAll, acc, CM] = aS.mtFileClassification(direc+wav_file, "svm_amlo_v1", "svm", True)
    print classesAll
    j = flagsInd
    l = classesAll 
    return j, l

df = pd.DataFrame(columns=['Position', 'Label', 'New_Label'])

def segment_file(direc, wav_file):
    
    global df
    num_labels = numpy.array(j).tolist()
    lst = range(0, len(num_labels))
    df['Position'] = lst
    df['Label'] = num_labels
    for index, row in df.iterrows(): 
        if df["Label"][index] == 0:
            df["Label"][index] = "amlo"
        else: 
            df["Label"][index] = "not_amlo"
    df["New_Label"] = df["Label"] +"_part"
    firstchange = 0
    counter = 0
    for index, row in df.iterrows():
        global firstchange, counter 
        if index == 0:
            pass
        elif df["Label"][index] != df["Label"][index-1] :
            firstchange = index 
            counter += 1
            df["New_Label"][index] = df["Label"][index] + str(counter)
        
        elif df["Label"][index] == df["Label"][firstchange]:
            df["New_Label"][index] = df["New_Label"][firstchange]
        else: 
            df["New_Label"][index] = df["New_Label"][index-1]
    df = df.loc[(df.Label == "amlo")]
    seg_list = list(df["New_Label"])    
    seg_list = list(set(seg_list))
    
    newpath = r'test//segmented//' + wav_file + "//"
    import os 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for clip in seg_list:
        print clip 
        temp_df = df.loc[(df.New_Label == clip)]
        beg = min(temp_df.Position)
        end = max(temp_df.Position)
        duration = str(end - beg)
        beg = str(min(temp_df.Position))
        end = str(max(temp_df.Position))
        print beg, end 
        command=  "ffmpeg -i " +direc+wav_file+ " -ss " +beg+ " -t " + duration+ " -acodec copy " + newpath+wav_file+clip+".wav" 
        
        subprocess.call(command, shell=True)
        print "added"

        
        
def process_files (direc):
    test_files = [f for f in listdir(direc) if isfile(join(direc, f))]
    print test_files
    for wav_file in test_files:
        new = conv_samp(direc, wav_file)
        aud_classify(direc, wav_file+".wav")

#process_files("test/")
conv_samp("test/", "amlo_mix.wav")
aud_classify("test/", "amlo_mix.wav.wav")
segment_file("test/", "amlo_mix.wav.wav")

##test with shorter mid-term windows              
#aS.hmmSegmentation('data/scottish.wav', 'amlo_hmm_short', True, 'data/scottish.segments')              

#python audioAnalysis.py trainHMMsegmenter_fromdir -i test/amlo_hmm/ -o amlo_hmm -mw 1.0 -ms 1.0
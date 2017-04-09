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
import psycopg2


#convert to 16000

def conv_samp(direc, wav_file):
    command = "ffmpeg -i " +direc+"/"+wav_file+ " -ac 1 -ab 44100 -ar 16000 " + direc+ wav_file +".wav" + " -y"
    subprocess.call(command, shell=True)

def trainSVM():
    aT.featureAndTrain(["amlo/","not_amlo"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "svm_amlo_no_music")    


def train():
    #train on several files 

    aT.featureAndTrain(["amlo/","not_amlo"], 1, 1, aT.shortTermWindow, aT.shortTermStep, "svm", "models/svm_full_step_nomusic")    
    #aT.featureAndTrain(["amlo/","not_amlo"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "randomforest", "models/randomforest_full_step")    

    ##try model with shorter mid-term windows

def add_to_DB(youID, clip, beg, end, duration, model):
    conn_string = "host='localhost' dbname='mexican_politics' user='presdb' password='dbpass'"
    print "Connecting to database\n	->%s" % (conn_string)
     
    conn = psycopg2.connect(conn_string)
     
    cursor = conn.cursor()
    
    for index, row in df.iterrows():
        sql = "INSERT INTO vid_segments(youID, speaker, start, endtime, duration, model) VALUES(%s, %s, %s, %s, %s, %s)"
        data = (youID, clip, beg, end, duration, model)
        cursor.execute(sql, data)
        conn.commit()


def aud_classify(direc, wav_file, model):
##test on one file                          
    global j, l
    print "classifying" + direc+wav_file
    [flagsInd, classesAll, acc, CM] = aS.mtFileClassification(direc+wav_file, "models/"+model, "svm", True)
    print classesAll
    j = flagsInd
    l = classesAll 

    return j, l, model


df = pd.DataFrame(columns=['VidID', 'Position', 'Label', 'New_Label'])

def segment_file(direc, wav_file, model):
    
    global df
    num_labels = numpy.array(j).tolist()
    lst = range(0, len(num_labels))
    [int(i) for i in num_labels]
    df['Position'] = lst
    df['Label'] = num_labels
    for index, row in df.iterrows(): 
        if df["Label"][index] == 0:
            df["Label"][index] = "amlo"
        else: 
            df["Label"][index] = "not_amlo"
    df["New_Label"] = df["Label"] 
    df["VidID"] = wav_file
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
    #df = df.loc[(df.Label == "amlo")]
    seg_list = list(df["New_Label"])    
    seg_list = list(set(seg_list))
    
    newpath = r'test//segmented//' + wav_file + "//"
    import os 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for clip in seg_list:
        print clip 
        temp_df = df.loc[(df.New_Label == clip)]
        vidID = df.VidID[1]
        
        beg = min(temp_df.Position)
        end = max(temp_df.Position)
        duration = str(end - beg)
        beg = str(min(temp_df.Position))
        end = str(max(temp_df.Position))
        print beg, end
        if duration > 5:
            command=  "ffmpeg -i " +direc+wav_file+ " -ss " +beg+ " -t " + duration+ " -acodec copy " + newpath+wav_file+clip+".wav" 
            subprocess.call(command, shell=True)
            print "added"
        else:
            print "too short to segement"
            pass 
        add_to_DB(vidID, clip, beg, end, duration, model)
    df = pd.DataFrame(columns=['VidID', 'Position', 'Label', 'New_Label'])

      
        
def process_files (direc, model):
    test_files = [f for f in listdir(direc) if isfile(join(direc, f))]
    print test_files
    for wav_file in test_files:
        new = conv_samp(direc, wav_file)
        aud_classify(direc, wav_file+".wav", model)
        segment_file(direc, wav_file+".wav", model)
        
        
def conv_train (direc):
    train_files = [f for f in listdir(direc) if isfile(join(direc, f))]
    print train_files
    for wav_file in train_files:
        new = conv_samp(direc, wav_file)

#model = "svm_full_step"
#
#process_files("test/", model)
#
train()

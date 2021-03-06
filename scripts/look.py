# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 17:39:47 2018

@author: ning
"""

import os
import pandas as pd
os.chdir('D:\\NING - spindle\\OMG_collaborate_project\\CSVs\\')
transcript_train = pd.read_csv('omg_TrainTranscripts.csv')
Video_train = pd.read_csv('omg_TrainVideos.csv')
import matplotlib.pyplot as plt
import seaborn as sns

# print the columns of the video dataframe
Video_train.columns
# compute the duration of each video
Video_train['duration'] = Video_train['end'] - Video_train['start']
# pairwise plotting
#sns.pairplot(Video_train,hue='EmotionMaxVote')# huge image
sns.pairplot(Video_train[['utterance', 'arousal', 'valence','duration','EmotionMaxVote']],hue='EmotionMaxVote')
# concatenate the two dataframes
df = pd.concat([transcript_train,Video_train],axis=1)
df = df.T.drop_duplicates().T
# get the annotation folder and its subfolders
annotation_folder = 'D:\\NING - spindle\\OMG_collaborate_project\\DetailedAnnotation\\train\\'
os.listdir(annotation_folder)
# print the number of videos and links
print('# of video:',len(pd.unique(df['video'])),', # of link:',len(pd.unique(df['link'])))
# more video than link, so we will have one link corresponds to multiple video ID
# let's see the unique pairs of video and link
video_link = []
for ii,((v,l),d) in enumerate(df.groupby(['video','link'])):# 231 independent data frame
    video_link.append([v,l])

# subsample 100 from the full dataset
samples = df.sample(100)
sns.pairplot(samples[['utterance', 'arousal', 'valence','duration','EmotionMaxVote']],hue='EmotionMaxVote')

from sklearn.preprocessing import LabelEncoder
df['encode'] = LabelEncoder().fit_transform(df['link'])# different computer might encode the links differently

# download videos and we will cut the video according to the starts and stops from the dataframe
from pytube import YouTube #https://github.com/nficano/pytube
from tqdm import tqdm
#where to save
SAVE_PATH = "D:/OMG" #to_do
links =  pd.unique(df['link'])# 125 unique videos
names = pd.unique(df['encode'])# 125 unique names in numbers
for link,name in tqdm(zip(links,names)):
    try:
        #object creation using YouTube which was imported in the beginning
        yt = YouTube(link)
    except:
        print("Connection Error") #to handle exception
     
    #filters out all the files with "mp4" extension
    mp4files = (yt.streams
                  .filter(progressive=True, file_extension='mp4')
                  .order_by('resolution')
                  .desc()
                  .first())
    
    try:
        #downloading the video
        mp4files.download(SAVE_PATH,filename='%d.mp4'%name)
    except:
        print("Some Error!")
print('Task Completed!')

































































































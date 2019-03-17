#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 16:39:14 2019

@author: simeon
"""

import os,random,time,sys
import pygame

def play_sound_GE():
    sounds_folder = "Sounds/"
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(sounds_folder+"good-evening.wav")
    pygame.mixer.music.play()

def play_song():
    mp3s = []
    mediapath = "Music/"
    for path,directory,element in os.walk(mediapath,False):
    	print("Loading music from" + path + "...")
    	tmparray = element

    	for i in range(0,len(tmparray)):
    		if(tmparray[i][-3:] == "mp3" and tmparray[i][:1] != "."):
    			mp3s.append(tmparray[i])
    		else:
    			print("Unuseable:",tmparray[i])
    
    	print("Loaded " + str(len(mp3s)) + " files, of " + str(len(element)) + " total")
    
    random.shuffle(mp3s)
    pygame.init()
    pygame.mixer.init()
    song_number=0
    pygame.mixer.music.load(mediapath+mp3s[0])
    pygame.mixer.music.play()
    return song_number, mp3s

def next_song(mp3s, song_number):
    try:
        mediapath = "Music/"
        song_number=song_number+1
        pygame.mixer.music.load(mediapath+mp3s[song_number])
        pygame.mixer.music.play()
        return song_number
    except:
        play_song()

def stop_music():
    pygame.mixer.music.stop()
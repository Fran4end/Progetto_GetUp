from distutils import file_util
from importlib.metadata import files
import time
from gtts import gTTS
import playsound as pl
import os

def textToAudioIt(str):
    audio = gTTS(str, lang='it')
    audio.save('./sample1.mp3')

def textToAudioEn(str):
    audio = gTTS(str, lang='en')
    audio.save('./sample2.mp3')

def ferm(str):
    audio = gTTS(str, lang='it')
    audio.save('./sample3.mp3')


t = 'Santa Lucia'
y = 'Bissuola Tevere'

def audio(nome, next):
    if(next):
        textToAudioIt('Prossima fermata, ')
        textToAudioEn('next stop, ')        
    else:
        textToAudioIt('Fermata, ' )
        textToAudioEn('Stop, ' )
    ferm(nome)
    pl.playsound('sample1.mp3')
    pl.playsound('sample3.mp3')
    pl.playsound('sample2.mp3')
    pl.playsound('sample3.mp3')
    os.remove('sample1.mp3')
    os.remove('sample2.mp3')
    os.remove('sample3.mp3')


audio(t, False)

time.sleep(2)

audio(y, True)
from ast import Constant
from distutils import file_util
from importlib.metadata import files
import time
from gtts import gTTS
import playsound as pl
import os

Constant.FERMATA = './sample3.mp3'
Constant.IT = './sample1.mp3'
Constant.EN = './sample2.mp3'

def text_to_audio_it(str):
    audio = gTTS(str, lang='it')
    audio.save(Constant.IT)

def text_to_audio_en(str):
    audio = gTTS(str, lang='en')
    audio.save(Constant.EN)

def ferm(str):
    audio = gTTS(str, lang='it')
    audio.save(Constant.FERMATA)


t = 'Santa Lucia'
y = 'Bissuola Tevere'

def audio(nome, next):
    if(next):
        text_to_audio_it('Prossima fermata, ')
        text_to_audio_en('next stop, ')        
    else:
        text_to_audio_it('Fermata, ' )
        text_to_audio_en('Stop, ' )
    ferm(nome)

    pl.playsound(Constant.IT)
    pl.playsound(Constant.FERMATA)
    pl.playsound(Constant.EN)
    pl.playsound(Constant.FERMATA)
    os.remove(Constant.IT)
    os.remove(Constant.EN)
    os.remove(Constant.FERMATA)


audio(t, False)

time.sleep(2)

audio(y, True)
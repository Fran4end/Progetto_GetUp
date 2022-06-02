from ast import Constant
from distutils import file_util
from importlib.metadata import files
import time
from gtts import gTTS
import pygame
import os

Constant.FERMATA = 'sample3.mp3'
Constant.IT = 'sample1.mp3'
Constant.EN = 'sample2.mp3'

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


def play(nome):
    pygame.mixer.init()
    sound = pygame.mixer.music.load(nome)
    playing = pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.delay(100)


def audio(nome, next):
    if(next):
        text_to_audio_it('Prossima fermata, ')
        text_to_audio_en('next stop, ')        
    else:
        text_to_audio_it('Fermata, ' )
        text_to_audio_en('Stop, ' )
    ferm(nome)

    play(Constant.IT)
    play(Constant.FERMATA)
    play(Constant.EN)
    play(Constant.FERMATA)


audio(t, False)
time.sleep(2)
audio(y, True)

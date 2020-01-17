#! /usr/bin/python3
# -*- coding: UTF-8 -*-

from music import *
from image import *
from random import *

import sys

sys.path.insert(0, "./jythonMusic/library/")
sys.path.insert(0, "./jythonMusic/library/jython2.5.3/Lib")

soundscapeScore = Score("Loutraki Soundscape", 60)
soundscapePart = Part(PIANO, 0)

scale = MIXOLYDIAN_SCALE

minPitch = 0  # MIDI pitch (0-127)
maxPitch = 127

minDuration = 0.8  # duration (1.0 is QN)
maxDuration = 6.0

minVolume = 0  # MIDI velocity (0-127)
maxVolume = 127

timeDisplacement = [DEN, EN, SN, TN]

params = sys.argv[2].split(';')
print(params)
image = Image(params)

pixelRows = [0, 53, 106, 159, 212]
width = image.getWidth()
height = image.getHeight()

def sonifyPixel(pixel):
    red, green, blue = pixel

    luminosity = (red + green + blue) / 3

    pitch = mapScale(luminosity, 0, 255, minPitch, maxPitch, scale)

    duration = mapValue(red, 0, 255, minDuration, maxDuration)

    dynamic = mapValue(blue, 0, 255, minVolume, maxVolume)

    note = Note(pitch, duration, dynamic)

    return note

for row in pixelRows:

    for col in range(width):

        pixel = image.getPixel(col, row)

        note = sonifyPixel(pixel)

        startTime = float(col)

        startTime = startTime + choice(timeDisplacement)

        phrase = Phrase(startTime)
        phrase.addNote(note)

        soundscapePart.addPhrase(phrase)


soundscapeScore.addPart(soundscapePart)

Write.midi(soundscapeScore, params[1])
sys.exit(0)
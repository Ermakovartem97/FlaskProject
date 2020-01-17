#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import sys

sys.path.insert(0, "./jythonMusic/library/")
sys.path.insert(0, "./jythonMusic/library/jython2.5.3/Lib")

from music import *
from string import *

# Читаем данные
params = sys.argv[2].split(';')
data = open(params [0], "r")

skinData = []
heartData = []
for line in data:
    
   time, skin, heart = split(line)  # Записываем данные в переменные
   skin = float(skin)               # Преобразуем полученные данные
   heart = float(heart)
   skinData.append(skin)            # Добавляем в массивы
   heartData.append(heart)

data.close()

##### Объявляем структуру
biomusicScore  = Score("Biosignal sonification", 150) #Задаём название и темп произведения 150 bpm
biomusicPart   = Part(PIANO, 0) #Партия пианино на 0 канале
biomusicPhrase = Phrase() #Создаём партию

# Находим критические значения
heartMinValue = min(heartData)
heartMaxValue = max(heartData)
skinMinValue   = min(skinData)
skinMaxValue   = max(skinData)

# Преобразуем данные
i = 0; 
while i < len(heartData):
 
   # Создаём ноты от минимального значения до даксимального в диапазоне от C3 до C6 в тональности C4
   pitch = mapScale(skinData[i], skinMinValue, skinMaxValue, C3, C6, 
                    MAJOR_SCALE, C4)
   # То же самое делаем для других данных, только уже берём другой диапазон
   pitchVariation = mapScale(heartData[i], heartMinValue, 
                             heartMaxValue, 0, 24, MAJOR_SCALE, C4)
 
   #dynamic = mapValue(heartData[i], heartMinValue, heartMaxValue, 0, 127)
    
   # Всё записываем в блокнот
   note = Note(pitch + pitchVariation, TN)

   biomusicPhrase.addNote(note)

   i = i + 1

##### Соединяем
biomusicPart.addPhrase(biomusicPhrase)
biomusicScore.addPart(biomusicPart)

##### Сохраняем и воспроизводим
Write.midi(biomusicScore, params[1])
sys.exit(0)
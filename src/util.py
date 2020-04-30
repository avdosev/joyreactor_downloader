# import csv
# import unicodecsv as csv
import re
import datetime
from time import sleep, time
import sys
from PIL import Image

# Убирает ватермарку, если она есть
def cleanWatermark(image_name):
    print("Убираем ватермарку с "+image_name)
    image = Image.open(image_name)
    sumR = sumG = sumB = 0
    for x in range(image.width):
        pixel = image.getpixel((x, image.height - 1))
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]
        sumR += r
        sumG += g
        sumB += b
    meanR = sumR / image.width
    meanG = sumG / image.width
    meanB = sumB / image.width
    # норма для ватермарки- 252,196,51
    isWatermarked = (meanR > 250 and meanR < 254 and
        meanG > 194 and meanG < 198 and
        meanB > 49 and meanB < 53)
    if isWatermarked:
        cropped = image.crop((0, 0, image.width-1, image.height-15))
        if getExtention(image_name) in ["jpg", "jpeg"]:
            cropped.save(convertNameToPng(image_name))
        else:
            cropped.save(image_name)
        return True
    else:
        return False

# Убирает формат и ставит вместо него png
def convertNameToPng(image_name):
    replaceAfter(image_name, '.', 'png')

def replaceAfter(string:str, symbol:str, replace_with:str):
    i = 0
    while(string[-i]!=symbol):
        i+=1
    return string[:-i+1] + replace_with

# Вычленяет расширение картинки из её url
def getExtention(url):
    return getLastFrom(url, '.')

# Вычленяет имя картинки из её url
def getName(url):
    return getLastFrom(url, '/')

# Выдаёт подстроку после последнего вхождения данного символа
def getLastFrom(string:str, symbol: str):
    i = len(string) - 1
    while(string[i]!=symbol):
        i-=1
    return string[i+1:]

# Обрезает подстроку после последнего вхождения данного символа
def cutLastFrom(string:str, symbol: str):
    i = len(string) - 1
    while(string[i]!=symbol):
        i-=1
    return string[:i]
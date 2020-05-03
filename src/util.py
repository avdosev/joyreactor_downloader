import aiofiles
import os

# Убирает формат и ставит вместо него png
def convertNameToPng(image_name):
    replaceAfter(image_name, '.', 'png')


def replaceAfter(string:str, symbol:str, replace_with:str):
    i = string.rfind(symbol)
    return string[:-i+1] + replace_with


# Вычленяет расширение картинки из её url
def getExtention(url):
    return getLastFrom(url, '.')


# Вычленяет имя картинки из её url
def getName(url):
    return getLastFrom(url, '/')


# Выдаёт подстроку после последнего вхождения данного символа
def getLastFrom(string: str, symbol: str):
    i = string.rfind(symbol)
    return string[i+1:]


# Обрезает подстроку после последнего вхождения данного символа
def cutLastFrom(string: str, symbol: str):
    i = string.rfind(symbol)
    return string[:i]


async def append_to_file(arr, filename: str, separator='\n'):
    async with aiofiles.open(filename, "a") as f:
        for element in arr:
            await f.write(element + separator)

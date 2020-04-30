import os
import asyncio
import aiohttp
from asyncio.futures import Future
from typing import List
from PIL import Image
from safe_get import safe_get

from util import *

# 2.1 Обработка урлов — удаление дубликатов и уже скачанных
# удаление дубликатов не нужно, ибо используются set'ы
# 2.2 Скачивание картинок по урлам
# 2.2.1 скачивание картинок
# 2.2.2 запись урлов скачанных картинок в downloaded
# 2.3 Обрезание ватермарки

# формат файлов:
# файл с запрещёнными картинками содержит урлы постов
# файл со скачанными картинками содержит ИМЕНА картинок, не урлы

# записывает список файлов из path в файл filename
def get_downloaded_names(filename, path="."):
    name_list = list(filter(lambda x: getExtention(x).lower() in ["jpg", "jpeg", "png", "bmp", "gif"], os.listdir(path)))
    with open(filename, "a", encoding='utf-8') as f:
        for e in name_list:
            f.write(e + '\n')

# удаляет из первого списка урлы, имена файлов которых есть во втором
def remove_downloaded(url_list, downloaded_names):
    i = 0
    while i < len(url_list):
        if getName(url_list[i]) in downloaded_names:
            del url_list[i]

# получает очищенные от дубликатов урлы, по которым можно качать
def get_urls_to_download(url_filename, downloaded_filename):
    urls = list(set(readFile(url_filename))) # нужно для проверки уникальности
    downloaded = set(readFile(downloaded_filename))
    remove_downloaded(urls, downloaded)
    return urls

# скачивает картинки по переданным ссылкам
# проверки уникальности не выполняются
def downloadFromLinks(links):
    new_links = []
    broken_links = []
    with open("logs/downloaded.txt", "a") as f:
        for link in links:
            filename = downloadImage(link)
            if filename is not None:
                cleanWatermark(filename)
                new_links.append(link)
            else:
                broken_links.append(link)
    with open("logs/downloaded.txt", "a") as f:
        for link in new_links:
            f.write(link+'\n')
    with open("logs/broken.txt", "a") as f:
        for link in broken_links:
            f.write(link+'\n')   
    return True

# Скачивает картинку по ссылке
def downloadImage(url, name=""):
    print("Качаем " + url)
    req = safe_get(url)
    if (req.status_code != 200):
        print("Запрос к " + url + " завершился с кодом " + req.status_code)
        return None
    filename = "i/"+name+getName(url)
    out = open(filename, "wb")
    out.write(req.content)
    out.close()
    return filename

# Убирает ватермарку, если она есть
def cleanWatermark(image_name):
    print("Убираем ватермарку с "+image_name)
    image = Image.open(image_name)
    # определяем, есть ли ватермарка
    # это определяется по среднему цвету нижних пикселей
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
    isWatermarked = (abs(meanR - 252) < 2 and abs(meanG - 196) < 2 and abs(meanB - 51) < 2)
    if isWatermarked:
        if getExtention(image_name).lower() in ["jpg", "jpeg", "png", "bmp"]: # GIF здесь нет, я пока хз, как их обрабатывать
            cropped = image.crop((0, 0, image.width-1, image.height-15))
            if getExtention(image_name) in ["jpg", "jpeg"]:
                cropped.save(convertNameToPng(image_name))
            else:
                cropped.save(image_name)
            return 'cropped'
        else:
            return 'unknown format'
    else:
        return 'no watermark'
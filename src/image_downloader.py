import os
import asyncio
import aiohttp
import aiofiles
from asyncio.futures import Future
from typing import List

from safe_get import safe_get
from image_util import cleanWatermark
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
    name_list = list(
        filter(lambda x: getExtention(x).lower() in ["jpg", "jpeg", "png", "bmp", "gif"], os.listdir(path)))
    with open(filename, "a", encoding='utf-8') as f:
        for e in name_list:
            f.write(e + '\n')


# получает очищенные от дубликатов урлы, по которым можно качать
def get_urls_to_download(url_filename, downloaded_filename):
    with open(url_filename, 'r') as f, open(downloaded_filename, 'r') as f2:
        urls = set(f)  # нужно для проверки уникальности
        downloaded = set(f2)
        return list(urls - downloaded)


# скачивает картинки по переданным ссылкам
# проверки уникальности не выполняются
def downloadFromLinks(links):
    new_links = []
    broken_links = []
    with open("logs/downloaded.txt", "a") as f:
        for link in links:
            filename = download_image(link)
            if filename is not None:
                cleanWatermark(filename)
                new_links.append(link)
            else:
                broken_links.append(link)
    with open("logs/downloaded.txt", "a") as f:
        for link in new_links:
            f.write(link + '\n')
    with open("logs/broken.txt", "a") as f:
        for link in broken_links:
            f.write(link + '\n')
    return True


# Скачивает картинку по ссылке
async def download_image(url, session, filename, **kwargs):
    print("Качаем " + url)
    resp = await safe_get(url, session, **kwargs)
    if resp.status != 200:
        print("Запрос к " + url + " завершился с кодом " + resp.status)
        return False

    # "i/" + name + getName(url)
    async with aiofiles.open(filename, "wb") as out:
        await out.write(await resp.read())

    return True




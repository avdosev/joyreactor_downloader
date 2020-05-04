import os
import asyncio
import aiohttp
import aiofiles
from asyncio.futures import Future
from typing import List

from safe_get import safe_get
from image_util import clean_watermark
import io
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
    name_list = filter(lambda x: getExtention(x).lower() in ["jpg", "jpeg", "png", "bmp", "gif"], os.listdir(path))
    with open(filename, "a", encoding='utf-8') as f:
        for e in name_list:
            f.write(e + '\n')


# получает очищенные от дубликатов урлы, по которым можно качать
def get_urls_to_download(url_filename, downloaded_filename):
    with open(url_filename, 'r') as urls_file, \
            open(downloaded_filename, 'r') as download_urls_file:
        all_urls = set(urls_file)
        downloaded = set(download_urls_file)
        # получаем набор уникальных url
        return list(all_urls - downloaded)


# скачивает картинки по переданным ссылкам
# проверки уникальности не выполняются
async def download_by_links(links, session):
    new_links = []
    broken_links = []

    for link in links:
        filename = "i/" + getName(link) + ".png"
        try:
            with open(filename, 'wb') as out_image:
                clean_watermark(io.BytesIO(await download_image(link, session)), out_image)
                new_links.append(link)
        except aiohttp.ClientResponseError:
            print(f"На {link} мы соснули бибос")
            broken_links.append(link)

    await asyncio.gather(
        append_to_file(new_links, "logs/downloaded.txt"),
        append_to_file(broken_links, "logs/broken.txt")
    )


# Скачивает картинку по ссылке
async def download_image(url, session, **kwargs):
    print("Качаем " + url)
    resp = await safe_get(url, session, **kwargs)
    resp.raise_for_status()
    return await resp.read()




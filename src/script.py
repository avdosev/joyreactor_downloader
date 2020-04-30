from time import time as current_time
import os.path

import asyncio
from aiohttp import ClientSession

from util import getName, cutLastFrom, append_to_file
from reactor_parse import scrapPage, getPrevPages, parse_html
from safe_get import safeGet

LAST_REQUEST_TIME = current_time()
DEFAULT_WAIT_TIME = 0.1


# http://old.reactor.cc/tag/Anime

# download - качает указанные картинки
# saveSrc - сохраняет ссылки на указанные картинки
# bulk - при прерывании по Ctrl+C сохраняет наработки и при следующем вызове продолжает работу

async def bulk_save_source_image_by_tag(url):
    # считать прогресс
    # в файле записана последняя проверенная страница
    last_page_checked = url
    name = getName(url)

    filename = os.path.join("temp", f"{name}_bulkSaveSrc_imageFromTag.txt")

    if name in {"all", "best", "new"}:
        print(str.format("убираем {0}...", name))
        name = getName(cutLastFrom(url, '/'))
        print(str.format("получаем {0}", name))

    output_name = f"url_{name}.txt"
    if os.path.isfile(filename):  # если файла нет, то и прогресс не надо считывать
        print("найден файл прогресса")
        with open(filename, "r") as f:
            last_page_checked = f.read()
    else:
        print("файл прогресса не найден")

    if last_page_checked == "":
        last_page_checked = url
        print("файл прогресса пуст")
    else:
        print("продолжаем с ", last_page_checked)

    # продолжить
    async with ClientSession() as session:
        html = await download_parsed_page(last_page_checked, session)
        tag_pages_list = getPrevPages(url, html)
        try:
            for page in tag_pages_list:
                html = await download_parsed_page(page, session)
                result = scrapPage(html)
                src_list = result['links']
                censored_list = result['censored']
                # следующий кусок кода независимый друг от друга и мы можем выполнить их паралельно
                await asyncio.gather(*[
                    append_to_file(src_list, output_name),
                    append_to_censored(censored_list)
                ])
                last_page_checked = page
        except KeyboardInterrupt:
            with open(filename, "w") as f:
                print(f"Последняя страница", last_page_checked, "сохранена")
                f.write(last_page_checked)

async def append_to_censored(censored_links):
    await append_to_file(censored_links, "logs/censored.txt")

# Запрашивает страницу по адресу
async def download_parsed_page(url, session):
    print("Запрашиваем " + url)
    html_text = await safeGet(url, session)
    html = parse_html(html_text)
    return html


if __name__ == "__main__":
    asyncio.run(bulk_save_source_image_by_tag("http://old.reactor.cc/tag/Anime/all"))

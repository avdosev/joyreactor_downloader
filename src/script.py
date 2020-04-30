from time import time as current_time
import os.path

import asyncio
from aiohttp import ClientSession

from util import getName, cutLastFrom, append_to_file
from reactor_parse import scrapPage, getPrevPages, parse_html
from safe_get import fetch_html

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
            async def download_and_parse(page, session, queue):
                html = await download_parsed_page(page, session)
                result = scrapPage(html)
                src_list = result['links']
                censored_list = result['censored']
                await queue.put((src_list, censored_list, page))

            async def load_parsed_data_to_file(queue):
                nonlocal last_page_checked
                while True:
                    src_list, censored_list, page = await queue.get()
                    last_page_checked = page
                    # следующий кусок кода независимый друг от друга и мы можем выполнить их паралельно
                    await asyncio.gather(*[
                        append_to_file(src_list, output_name),
                        append_to_censored(censored_list)
                    ])
                    queue.task_done()

            queue = asyncio.Queue()
            producers = [asyncio.create_task(download_and_parse(page, session, queue)) for page in tag_pages_list]
            file_loader = asyncio.create_task(load_parsed_data_to_file(queue))
            await asyncio.gather(*producers)
            await queue.join()
            file_loader.cancel()
            await asyncio.gather(file_loader, return_exceptions=True)
        except KeyboardInterrupt:
            with open(filename, "w") as f:
                print(f"Последняя страница ", last_page_checked, " сохранена")
                f.write(last_page_checked)

async def append_to_censored(censored_links):
    await append_to_file(censored_links, "logs/censored.txt")

# Запрашивает страницу по адресу
async def download_parsed_page(url, session):
    print("Запрашиваем " + url)
    html_text = await fetch_html(url, session)
    html = parse_html(html_text)
    return html

if __name__ == "__main__":
    asyncio.run(bulk_save_source_image_by_tag("http://old.reactor.cc/tag/Anime/all"))

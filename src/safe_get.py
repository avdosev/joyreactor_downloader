from time import time as current_time
import asyncio
from aiohttp import ClientSession

# файл для запросов к серверу

LAST_REQUEST_TIME = current_time()
DEFAULT_WAIT_TIME = 1.5
DOWNLOAD_LOCK = asyncio.Lock()

async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """
    GET запрос оболочки для загрузки страницы HTML.
    kwargs передаются в session.request().
    """
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    html = await resp.text()
    return html

# Делает запрос с учётом времени между запросами
async def safeGet(url, session, wait_time = DEFAULT_WAIT_TIME):
    global LAST_REQUEST_TIME

    await DOWNLOAD_LOCK.acquire()

    time_from_last_request = current_time() - LAST_REQUEST_TIME
    # по логике, это значение не должно быть отрицательным
    # можно вставить проверку, но даже если оно будет отрицательным, всё должно норм работать

    if time_from_last_request < wait_time:
        await asyncio.sleep(wait_time - time_from_last_request)

    LAST_REQUEST_TIME = current_time()
    result = await fetch_html(url, session)
    DOWNLOAD_LOCK.release()

    return result
import io
import time
import requests
from utils.image_util import clean_watermark
from utils.url import gen_url
import os
import shutil

def download_image(key, output_dir, cache_dir):
    try:
    # if True:
        url = gen_url(key)
        cache_img = f'{cache_dir}/{key}.jpeg'
        output_img = f'{output_dir}/{key}.jpeg'

        if not os.path.exists(cache_img):
            resp = requests.get(url)
            out_buff = io.BytesIO()
            clean_watermark(io.BytesIO(resp.content), out_buff)
            with open(cache_img, 'wb') as f:
                f.write(out_buff.getvalue())
        shutil.copy(cache_img, output_img)
    except:
        print('failed:', url)
    
    time.sleep(1.5)


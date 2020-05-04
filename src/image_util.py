from PIL import Image
from util import *
import io


# Убирает ватермарку, если она есть
def clean_watermark(image_io: io.BinaryIO, out_io: io.BinaryIO):
    image = Image.open(image_io)
    # определяем, есть ли ватермарка
    # это определяется по среднему цвету нижних пикселей
    sumR = sumG = sumB = 0
    # TODO: Maybe using numpy or opencv
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
        if image.format().lower() in ["jpg",
                                      "jpeg",
                                      "png",
                                      "bmp"]:  # GIF здесь нет, я пока хз, как их обрабатывать
            cropped = image.crop((0, 0, image.width - 1, image.height - 15))
            cropped.save(out_io, 'png', quality=100)
            return 'cropped'
        else:
            return 'unknown format'
    else:
        return 'no watermark'
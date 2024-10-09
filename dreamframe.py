import base64
from functools import reduce
import logging
import requests
import io

from PIL import Image

from waveshare_epd import epd7in3e

URL = 'http://192.168.50.245:5000'

palette = reduce(lambda x, y: x + y, [
    (0x00, 0x00, 0x00),  # black
    (0xff, 0xff, 0xff),  # white
    (0x00, 0xff, 0xff),  # yellow
    (0x00, 0x00, 0xff),  # red
    (0xff, 0x00, 0x00),  # blue
    (0x00, 0xff, 0x00),  # green
])

palette_string = base64.urlsafe_b64encode(bytearray(palette))

palette_image = Image.new('P', (1, 1))
palette_image.putpalette(palette)

logging.basicConfig(level=logging.DEBUG)

try:
    response = requests.get(url=f'{URL}/api/generate', params={
        'h': 480,  # epd.height,
        'w': 800,  # epd.width,
        'palette': palette_string,
    })

    Himage = Image.open(io.BytesIO(response.content))

    # Himage.show()

    epd = epd7in3e.EPD()
    epd.init()
    epd.Clear()
    epd.display(epd.getbuffer(Himage))

    logging.info("Goto Sleep...")

    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in3e.epdconfig.module_exit(cleanup=True)  # type: ignore
    exit()

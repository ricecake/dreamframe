import logging
import requests
import io

from PIL import Image

from waveshare_epd import epd7in3e

URL = 'http://192.168.50.245:5000'

logging.basicConfig(level=logging.DEBUG)

try:

    response = requests.get(url=f'{URL}/api/generate', params={
        'h': 480,  # epd.height,
        'w': 800,  # epd.width,
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
    epd7in3e.epdconfig.module_exit(cleanup=True)
    exit()

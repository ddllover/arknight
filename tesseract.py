"""
from PIL import Image
import pytesseract

img = Image.open('C:/Users/wangyan/Desktop/1.png')
text = pytesseract.run_and_get_output(img,lang='chi_sim')
print(text)
#print(pytesseract.get_languages( config = '' ))
"""
import configparser
import logging

logger = logging.getLogger(__name__)
config=configparser.ConfigParser()
config.read('config.ini')
config=config['start']
print(config['skip_png'])
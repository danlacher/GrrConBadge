#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import time
import requests
import re
import math

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V4
from PIL import Image,ImageDraw,ImageFont
import traceback

URL = "https://pspipegrep.com/grrcon2025/submissions.txt"
BADWORDS_FILE = "bad-words.txt"

def load_bad_words(filepath:str):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def censor_text(text: str, bad_words):
    """Replace whole bad words in text with hash symbols."""
    for word in bad_words:
        # Match whole words only (case insensitive)
        pattern = re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
        text = pattern.sub("#" * len(word), text)
    return text

def chunk_text(text: str, chunk_size: int = 18):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def Refresh_Display(epd, string):
    epd.init()
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), ' /dev/null', font = font15, fill = 0)
    draw.text((190, 0), time.strftime('%H:%M:%S'), font = font15, fill = 0)

    starting_offset = 25
    count = 1

    ctf_string="We're the dot in DotCOM"
    if ctf_string in string:
        string = string.replace(ctf_string, "#WINNER")

    chunks = chunk_text(string, 24)
    for chunk in chunks:
        draw.text((0, (count * starting_offset)), chunk, font = font24, fill = 0)
        count += 1

    image = image.rotate(180) # rotate
    return image

try:
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    shown_lines = set()

    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    bad_words = load_bad_words(BADWORDS_FILE)

    mystring = 'INIT...'
    epd.display(epd.getbuffer(Refresh_Display(epd, mystring)))
    time.sleep(1)

    while (True):
        response = requests.get(URL)
        response.raise_for_status()
        lines = response.text.splitlines()
        for line in lines:
            line = line.strip()
            if line and line not in shown_lines:
                clean_line = censor_text(line, bad_words)
                epd.display(epd.getbuffer(Refresh_Display(epd, clean_line)))
                shown_lines.add(clean_line)
                time.sleep(5)

    #logging.info("Clear...")
    epd.init()
    epd.Clear(0xFF)

    #logging.info("Goto Sleep...")
    epd.sleep()

except Exception as e:
    print(f"Error fetching file: {e}")
    # wait 60 seconds before pulling the file again
    time.sleep(60)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    #logging.info("ctrl + c:")
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()

from message_handling_base import *

import sys
import random
import discord
import re
import unicornhathd
import threading
from matrix_images import *
import time
import math
from datetime import datetime, timedelta
import colorsys
from PIL import Image, ImageDraw, ImageFont
from sys import exit

eyes_thread = None
scroll_thread = None

unicornhathd.rotation(270)


class ShutdownHandler(MatchingMessageHandler):
    def __init__(self, client, trigger_msg):
        super().__init__(
            client,
            terminates=True,
            must_equal=trigger_msg
        )

    async def handle_message(self, msg):
        await msg.channel.send("Bye!")
        await self.client.close()
        sys.exit()


class Magic8Ball(MatchingMessageHandler):
    def __init__(self, client):
        super().__init__(
            client,
            terminates=True,
            must_start_with="cubot,",
            must_end_with="?"
        )

        file = open("resources/text/8ball-responses.txt")
        self.magic_responses = file.readlines()
        file.close()

    async def handle_message(self, msg):
        random.seed(hash(msg.lower))
        await msg.channel.send(random.choice(self.magic_responses))

        # restore random seed value
        random.seed()


class EyyHandler(MatchingMessageHandler):
    def __init__(self, client):
        super().__init__(
            client,
            start_must_match=r"\b(a|e)y+\b"
        )

        self.y_counters = {"a": 0, "e": 0}

    async def handle_message(self, msg):
        first_char = msg.lower[0]
        eyy_length = len(self.start_must_match.match(msg.lower).group(0)) - 1
        self.y_counters[first_char] += eyy_length
        response = first_char + ("y" * self.y_counters[first_char])

        # limit to 2000 characters
        response = response[:min(len(response), 2000)]

        if msg.raw[:eyy_length].isupper():
            response = response.upper()

        await msg.channel.send(response)


class EyesHandler(MatchingMessageHandler):
    def __init__(self, client):
        super().__init__(
            client,
            must_contain=["👀"]
        )


    def shake_eyes_on_matrix(self):
        global eyes_thread

        unicornhathd.brightness(0.6)
        unicornhathd.clear()

        for x in range(unicornhathd.WIDTH):
            for y in range(unicornhathd.HEIGHT):
                r, g, b = eyes_image[x][y]
                unicornhathd.set_pixel(x, y, r, g, b)

        unicornhathd.show()
        # time.sleep(0.5 / 32)

        t_end = time.time() + 5
        while time.time() < t_end:
            angle = random.uniform(0, math.pi * 2)
            dist = random.uniform(0, 2)

            for x in range(unicornhathd.WIDTH):
                for y in range(unicornhathd.HEIGHT):
                    r, g, b = eyes_image[x][y]

                    try:
                        x_offset = round(math.cos(angle) * dist)
                        y_offset = round(math.sin(angle) * dist)
                        unicornhathd.set_pixel(x + x_offset, y + y_offset, r, g, b)
                    except:
                        pass

            unicornhathd.show()
            # time.sleep(0.5 / 32)

        unicornhathd.off()

        eyes_thread = None

    async def handle_message(self, msg):
        global eyes_thread

        await msg.obj.add_reaction("👀")

        if eyes_thread is None:
            # start matrix eye shaking thread
            eyes_thread = threading.Thread(target=self.shake_eyes_on_matrix)
            eyes_thread.start()


class MatrixTextHandler(MatchingMessageHandler):
    def __init__(self, client):
        super().__init__(
            client,
            must_start_with="!scroll "
        )


    def scroll_text_on_matrix(self, scroll_text):
        t = threading.current_thread()

        colour = (255, 0, 0)
        FONT = ('/usr/share/fonts/truetype/freefont/FreeSansBold.ttf', 16)

        unicornhathd.brightness(0.6)
        unicornhathd.clear()

        width, height = unicornhathd.get_shape()

        text_x = width
        text_y = 0

        font_file, font_size = FONT

        font = ImageFont.truetype(font_file, font_size)

        text_width, text_height = width, 0

        try:
            w, h = font.getsize(scroll_text)
            text_width += w + width
            text_height = max(text_height, h)

            text_width += width + text_x + 1

            image = Image.new('RGB', (text_width, max(16, text_height)), (0, 0, 0))
            draw = ImageDraw.Draw(image)

            offset_left = 0

            draw.text((text_x + offset_left, text_y), scroll_text, colour, font=font)

            offset_left += font.getsize(scroll_text)[0] + width

            while getattr(t, "running", True):
                for scroll in range(text_width - width):
                    for x in range(width):
                        for y in range(height):
                            pixel = image.getpixel((x + scroll, y))
                            r, g, b = [int(n) for n in pixel]

                            if max(r, g, b) < 200:
                                r, g, b = (0, 0, 0)

                            unicornhathd.set_pixel(width - 1 - x, y, r, g, b)

                    unicornhathd.show()
                    time.sleep(0.015)

                time.sleep(1)

        except KeyboardInterrupt:
            unicornhathd.off()

        finally:
            unicornhathd.off()

    async def handle_message(self, msg):
        global scroll_thread

        scroll_text = msg.raw[8:].upper()
        # insert extra space between words
        scroll_text = "".join(c * 2 if c == " " else c for c in scroll_text)

        await msg.channel.send("Ok, setting LED matrix scroll text to \"{}\"".format(scroll_text))

        if scroll_thread is not None:
            scroll_thread.running = False
            scroll_thread.join()

        # start matrix text scrolling thread
        scroll_thread = threading.Thread(target=self.scroll_text_on_matrix, args=(scroll_text,))
        scroll_thread.start()


class LoveCubotHandler(MatchingMessageHandler):
    def __init__(self, client):
        super().__init__(
            client,
            must_contain=["love", "cubot"]
        )

    async def handle_message(self, msg):
        await msg.obj.add_reaction("❤")


class WokeHandler(MatchingMessageHandler):
    def __init__(self, client):
        super().__init__(
            client,
            must_match=r"(\((woke|w)\)(.*?)\((unwoke|uw)\))"
        )

    async def handle_message(self, msg):
        woke_strings = [" ".join(match[2].upper()) for match in re.findall(self.must_match, msg.lower)]
        response = "\n".join(woke_strings)
        await msg.channel.send(response)


class MathsHandler(MatchingMessageHandler):
    def __init__(self, client):
        super().__init__(
            client,
            must_match=r"(.*?)(\bmaths\b|mafematics)"
        )

    async def handle_message(self, msg):
        await msg.channel.send(file=discord.File("resources/media/mafematics.jpg"))


class ConversionHandler(MatchingMessageHandler):
    def __init__(self, client):
        super().__init__(
            client,
            must_match=r"cubot, (time|temp)convert (.*) to (freedom|nonfreedom) (units|time)"
        )

    async def handle_message(self, msg):
        type = self.must_match.match(msg.lower).group(1)
        value = self.must_match.match(msg.lower).group(2)
        unit = self.must_match.match(msg.lower).group(3)

        if type == 'temp':
            if unit == 'freedom':
                new_val = str(round((int(value) * (9/5)) + 32, 2))
                response = value + ' is ' + new_val + ' in freedom units'

            if unit == 'nonfreedom':
                new_val = str(round((int(value) - 32) * (5/9), 2))
                response = value + ' is ' + new_val + ' in nonfreedom units'

            await msg.channel.send(response)

        if type == 'time':
            match = re.search(r"(\d{1,2}:?)(\d{2})?(am|pm)", value)

            if match.group(1)[-1] == ':':
                hour = int(match.group(1)[0:len(match.group(1)) - 1])
                minute = int(match.group(2))
            if match.group(1)[-1] != ':':
                hour = int(match.group(1))
                minute = 0

            if match.group(3) == 'pm' and hour != 12:
                hour = hour + 12
            if match.group(3) == 'am' and hour == 12:
                hour = hour - 12

            dt_obj = datetime(2000, 1, 1, hour, minute, 0)

            if unit == 'freedom':
                new_time = dt_obj - timedelta(hours=5)
            if unit == 'nonfreedom':
                new_time = dt_obj + timedelta(hours=5)

            if new_time.hour > 12:
                new_hour = str(new_time.hour - 12)
                meridiem = 'pm'
            if new_time.hour <= 12:
                new_hour = str(new_time.hour)
                meridiem = 'am'

            if new_time.minute == 0:
                new_minute = '00'
            if new_time.minute != 0:
                new_minute = str(new_time.minute)

            response = match.group(0) + ' is ' + new_hour + ':' + new_minute + meridiem + ' in ' + unit + ' time'
            await msg.channel.send(response)

from message_handling_base import *

import sys
import random
import discord
import re
import unicornhathd
import time
import math
from datetime import datetime, timedelta


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

    async def handle_message(self, msg):
        await msg.obj.add_reaction("👀")

        unicornhathd.brightness(0.6)
        unicornhathd.clear()

        angles = [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi, 5*math.pi/4, 3*math.pi/2, 7*math.pi/4]

        pixels = list([[[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [255, 255, 255],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]],

               [[  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0],
                [  0,   0,   0]]])

        for x in range(unicornhathd.WIDTH):
            for y in range(unicornhathd.HEIGHT):
                r, g, b = pixels[x][y]
                unicornhathd.set_pixel(x, y, r, g, b)

        unicornhathd.show()
        time.sleep(0.5 / 32)

        t_end = time.time() + 5
        while time.time() < t_end:
            angle = random.choice(angles)
            dist = 2

            for x in range(unicornhathd.WIDTH):
                for y in range(unicornhathd.HEIGHT):
                    r, g, b = pixels[x][y]

                    try:
                        x_offset = math.round(math.cos(angle) * dist)
                        y_offset = math.round(math.sin(angle) * dist)
                        unicornhathd.set_pixel(x + x_offset, y_offset, r, g, b)
                    except:
                        pass

            unicornhathd.show()
            time.sleep(0.5 / 32)

            for x in range(unicornhathd.WIDTH):
                for y in range(unicornhathd.HEIGHT):
                    r, g, b = pixels[x][y]
                    unicornhathd.set_pixel(x, y, r, g, b)

            unicornhathd.show()
            time.sleep(0.5 / 32)


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

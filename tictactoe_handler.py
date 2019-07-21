from message_handling_base import *

import discord
import unicornhathd
from matrix_images import *

eyes_thread = None


class TicTacToeInitHandler(MatchingMessageHandler):
    def __init__(self, client, trigger_msg):
        super().__init__(
            client,
            terminates=True,
            must_match="((.*?) started the game, so they get the first move.)|"
        )

    async def handle_message(self, msg):
        await msg.channel.send("Bye!")
        await self.client.close()


class TicTacToeMoveHandler(MatchingMessageHandler):
    def __init__(self, client, trigger_msg):
        super().__init__(
            client,
            terminates=True,
            start_must_match="m! [A-I]"
        )

    async def handle_message(self, msg):
        await msg.channel.send("Bye!")
        await self.client.close()
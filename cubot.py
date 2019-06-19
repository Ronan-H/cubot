# Python 3

import discord
from cubot_message_handlers import init_handlers
from message_handling_base import Message

client = discord.Client()
handlers = init_handlers(client)

file = open('token.dat')
token = file.read()
file.close()

@client.event
async def on_message(message):
    # don't let cubot respond to himself
    if message.author == client.user:
        return

    msg_obj = Message(message)

    for handler in handlers:
        await handler.on_message(msg_obj)


@client.event
async def on_ready():
    logged_in_msg = "Logged in as " + client.user.name
    print(logged_in_msg)
    print("-" * len(logged_in_msg), end="\n\n")

print("Starting...", end="\n\n")
client.run(token)

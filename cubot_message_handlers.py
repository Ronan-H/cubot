from concrete_message_handlers import *


def init_handlers(client):
    handlers = [
        WokeHandler(client),
        Magic8Ball(client),
        EyesHandler(client),
        LoveCubotHandler(client),
        EyyHandler(client),
        ShutdownHandler(client, "cubot, shutdown"),
        MathsHandler(client),
        ConversionHandler(client)
    ]

    return handlers

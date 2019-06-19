import re


class Message:
    def __init__(self, msg):
        self.obj = msg
        self.channel = msg.channel
        self.raw = msg.content
        self.lower = self.raw.lower()


class MessageHandler:
    def __init__(self, client, terminates=False):
        self.client = client
        self.terminates = terminates

    async def on_message(self, msg):
        if self.should_handle_message(msg):
            await self.handle_message(msg)

            return self.terminates

        return False

    def should_handle_message(self, msg):
        return True

    def handle_message(self, msg):
        pass


class MatchingMessageHandler(MessageHandler):
    kwarg_defaults = {
        "must_equal": None,
        "must_start_with": "",
        "must_end_with": "",
        "must_contain": [],
        "must_match": r"(.*?)",
        "start_must_match": r"(.*?)",
        "use_msg_lower": True
    }

    def __init__(self, client, terminates=False, **kwargs):
        super().__init__(client, terminates)

        # ensure kwargs has no unexpected values
        for k in kwargs:
            if k not in self.kwarg_defaults:
                raise ValueError("Unknown kwarg \"{}\"".format(k))

        # apply kwarg defaults for arguments not specified
        for k in self.kwarg_defaults:
            if k not in kwargs:
                kwargs[k] = self.kwarg_defaults[k]

        # compile regex patterns
        kwargs["must_match"] = re.compile(kwargs["must_match"])
        kwargs["start_must_match"] = re.compile(kwargs["start_must_match"])

        self.__dict__.update(kwargs)

    def should_handle_message(self, msg):
        message = msg.lower if self.use_msg_lower else msg.raw

        if self.must_equal is not None:
            if not message == self.must_equal:
                return False

        if not message.startswith(self.must_start_with):
            return False

        if not message.endswith(self.must_end_with):
            return False

        for word in self.must_contain:
            if word not in message:
                return False

        if not self.must_match.search(message):
            return False

        if not self.start_must_match.match(message):
            return False

        return True
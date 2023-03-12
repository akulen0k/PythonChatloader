'''

Этот класс описывает канал

'''


from telethon.tl.types import Channel


class ChannelBd:

    def __init__(self, channel: Channel = None, lst: tuple = None):
        self.id = None
        self.channel_id = None
        self.handle = None
        self.title = None
        if channel is not None:
            self.channel_id = channel.id
            self.handle = '@' + channel.username
            self.title = channel.title
        if lst is not None:
            if len(lst) >= 1:
                self.id = lst[0]
            if len(lst) >= 2:
                self.channel_id = lst[1]
            if len(lst) >= 3:
                self.handle = lst[2]
            if len(lst) >= 4:
                self.title = lst[3]
        assert self.channel_id is not None and self.handle is not None and self.title is not None

    def getChannel(self):
        return f"({self.id}, {self.channel_id}, {self.handle}, {self.title})"

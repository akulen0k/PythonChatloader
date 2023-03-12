"""

Этот класс описывает сообщение, которое хранится в бд

"""
import telethon.tl.types.messages


class Message:

    def __init__(self, msg: telethon.types.Message = None, channel_id: int = -1, line: tuple = None):
        self.id = None
        self.channel_id = channel_id

        if msg is not None:
            self.message = msg.message
            self.date = msg.date

        if line is not None:
            self.id = line[0]
            self.channel_id = line[1]
            self.date = line[2]
            self.message = line[3]

        assert self.channel_id != -1

    def __str__(self):
        return f'({self.id}, {self.channel_id}, \'{self.date}\', \'{self.message}\')'

    def get_value(self):
        if id is None:
            return self.channel_id, self.date, self.message
        return self.id, self.channel_id, self.date, self.message


"""

Этот класс описывает запросы пользователей

"""


class Request:

    def __init__(self, lst: tuple):
        self.id = lst[0]
        self.url = lst[1]
        self.req = lst[2]
        self.resp = None
        self.answer = None
        self.status = None
        if len(lst) >= 4:
            self.resp = lst[3]
        if len(lst) >= 5:
            self.answer = lst[4]
        if len(lst) >= 6:
            self.status = lst[5]
        assert self.url is not None

    def get_value(self):
        if self.id is None:
            return self.url, self.req, self.resp, self.answer, self.status
        return self.id, self.url, self.req, self.resp, self.answer, self.status

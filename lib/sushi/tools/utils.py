from aiohttp import web


class Param:
    def parse(self, req: web.Request, params: dict) -> dict:
        pass


class Query(Param):
    def __init__(self, name: str, default, cls):
        self.name = name
        self.default = default
        self.cls = cls

    def parse(self, req: web.Request, params: dict) -> dict:
        params[self.name] = self.cls(req.query.get(self.name, self.default))
        return params

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

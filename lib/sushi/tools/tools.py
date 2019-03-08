import functools
from enum import Enum, auto, unique

from aiohttp import web

from lib.sushi.tools.handler import stats, health
from lib.sushi.tools.utils import Query, Param


def application():
    """
    Decorator applied to a class to mark an application.

    from sushi.tools import application, expose, parameter

    :example:
    @application()
    class Greeter(object):

        @expose(method="GET", path="/greet")
        @parameter(name="name")
        def greet(self, name):
            return "Hello " + name

    :param:
    :return: Wrapper class
    """
    class App(object):
        def __init__(self, cls):
            self._cls = cls

        def __call__(self, *args, **kwargs):
            self._paths = []
            self._app = web.Application()
            self._add_default_handlers()

            self._obj = self._cls(*args, **kwargs)

            for attrname in dir(self._obj):
                attr = getattr(self._obj, attrname)

                if not type(attr).__name__ == "ExposeDecorator":
                    continue

                self._build_handler(attr)

            return self

        def _build_handler(self, attr):

            async def handler(request: web.Request):
                resp = web.Response()
                kwargs = functools.reduce(lambda d, p: p.parse(request, d), attr.params, dict())

                resp.body = attr.func(self._obj, **kwargs)
                return resp

            self._register(attr.path, handler)

        def _add_default_handlers(self):

            async def paths(_):
                resp = web.Response()
                resp.body = "\n".join(self._paths)
                return resp

            self._register(path="/_/", handler=paths)
            self._register(path="/_/system", handler=stats)
            self._register(path="/_/health", handler=health)

        def _register(self, path, handler):
            self._paths.append(path)
            self._app.router.add_get(path=path, handler=handler)

        def run(self, *args, **kwargs):
            web.run_app(self._app, *args, **kwargs)

    return App


@unique
class HttpMethod(Enum):
    GET = "GET"


def expose(path: str, method: HttpMethod=HttpMethod.GET):

    class ExposeDecorator(object):
        def __init__(self, func):
            self.path = path
            self.method = method
            if func.__class__.__name__ == "ParameterDecorator":
                self.func = func.func
                self.params = func.params
            else:
                self.func = func
                self.params = []

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

    return ExposeDecorator


@unique
class ParamType(Enum):
    QUERY = auto()


def parameter(name: str, default=None, cls=str, method: ParamType=ParamType.QUERY):

    def _param():
        if method == ParamType.QUERY:
            return Query(name=name, cls=cls, default=default)

    class ParameterDecorator(object):

        def __init__(self, func):

            if func.__class__.__name__ == "ParameterDecorator":
                self.func = func.func
                self.params = func.params + [_param()]

            elif func.__class__.__name__ == "ExposeDecorator":
                raise ValueError("@expose must be top level decorator")

            else:
                self.func = func
                self.params = [_param()]

            if name not in self.func.__code__.co_varnames:
                raise ValueError("The param '%s' is not function argument for '%s'" % (name, self.func.__name__))

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

    return ParameterDecorator

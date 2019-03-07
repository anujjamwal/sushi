import functools


def application():
    """
    Decorator applied to a class to mark an application.

    from sushi.tools import application, expose, parameter

    :example:
    @application
    class Greeter(object):

        @expose(method="GET", path="/greet")
        @parameter(name="name")
        def greet(self, name):
            return "Hello " + name

    :param:
    :return: Wrapper class
    """
    pass


def expose(path, method="GET"):

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


def parameter(name, default=None, cls=str, method="query"):

    class ParameterDecorator(object):
        def __init__(self, func):
            if func.__class__.__name__ == "ParameterDecorator":
                self.func = func.func
                self.params = func.params + [dict(name=name, default=default, cls=cls, method=method)]
            elif func.__class__.__name__ == "ExposeDecorator":
                raise ValueError("@expose must be top level decorator")
            else:
                self.func = func
                self.params = [dict(name=name, default=default, cls=cls, method=method)]

            if name not in self.func.__code__.co_varnames:
                raise ValueError("The param '%s' is not function argument for '%s'" % (name, self.func.__name__))

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

    return ParameterDecorator

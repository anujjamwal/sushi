from lib.sushi.tools import application, expose, parameter, HttpMethod, ParamType


@application()
class Greeter(object):

    @expose(path="/greet", method=HttpMethod.GET)
    @parameter(name="name", method=ParamType.QUERY)
    def greet(self, name):
        return "Hello" + name


Greeter().run()
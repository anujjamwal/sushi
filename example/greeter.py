from sushi.tools import application, expose, parameter


@application
class Greeter(object):

    @expose(path="/greet", method="GET")
    @parameter(name="name", method="query")
    def greet(self, name):
        return "Hello" + name



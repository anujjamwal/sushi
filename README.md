# sushi

Sushi is an application engine for python apps

```python
from sushi.tools import application, expose, parameter


@application()
class Greeter(object):

    @expose(path="/greet", method="GET")
    @parameter(name="name", method="query")
    def greet(self, name):
        return "Hello" + name
```

```python
if __name__ == "__main__":
    app = Greeter()
    app.run()
```
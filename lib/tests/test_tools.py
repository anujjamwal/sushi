import unittest
from multiprocessing import Process
from threading import Thread

from lib.sushi.tools import HttpMethod
from lib.sushi.tools.utils import Query
from ..sushi.tools import parameter, expose, application


def pi():
    return 3.1415


def square(x):
    return x * x


def pow(x, y):
    return pow(x, y)


class TestParameter(unittest.TestCase):

    def test_parameter_to_store_params_in_decorator(self):
        wrapped_square = parameter(name="x")(square)
        params = wrapped_square.params

        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], Query(name="x", default=None, cls=str))

    def test_parameter_to_raise_error_if_param_unknown(self):
        self.assertRaises(ValueError, parameter(name="y"), square)

    def test_parameter_to_store_params_in_decorator_with_type(self):
        wrapped_square = parameter(name="x", cls=int)(square)
        params = wrapped_square.params

        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], Query(name="x", default=None, cls=int))

    def test_parameter_to_store_params_in_decorator_with_default(self):
        wrapped_square = parameter(name="x", default="y/m - c")(square)
        params = wrapped_square.params

        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], Query(name="x", default="y/m - c", cls=str))

    def test_parameter_to_wrap_parameter_wrapped_function(self):
        wrapped_pow = parameter(name="y", cls=int)(parameter(name="x", cls=int)(pow))
        params = wrapped_pow.params

        self.assertEqual(len(params), 2)
        self.assertEqual(params[0], Query(name="x", default=None, cls=int))
        self.assertEqual(params[1], Query(name="y", default=None, cls=int))


class TestExpose(unittest.TestCase):

    def test_expose_without_params(self):
        w = expose(path="/")(pi)
        self.assertEquals(w.path, "/")
        self.assertEquals(w.method, HttpMethod.GET)
        self.assertEquals(w.params, [])
        self.assertEquals(w.func, pi)

    def test_expose_without_params_with_method(self):
        w = expose(path="/pi", method=HttpMethod.POST)(pi)
        self.assertEquals(w.path, "/pi")
        self.assertEquals(w.method, HttpMethod.POST)
        self.assertEquals(w.params, [])
        self.assertEquals(w.func, pi)

    def test_expose_with_params_with_method(self):
        w = expose(path="/square")(parameter(name="x")(square))
        self.assertEquals(w.path, "/square")
        self.assertEquals(w.method, HttpMethod.GET)
        self.assertEquals(w.params, [Query(name="x", default=None, cls=str)])
        self.assertEquals(w.func, square)

    def test_params_with_expose(self):
        self.assertRaises(ValueError, parameter(name="y"), expose(path="/square")(square))


@application()
class Simple(object):
    @expose("/")
    @parameter(name="name")
    def greet(self, name):
        return "Hello " + name


class TestApplication(unittest.TestCase):
    p = Process(target=lambda: Simple().run())

    @classmethod
    def setUpClass(cls):
        cls.p.start()

    @classmethod
    def tearDownClass(cls):
        cls.p.terminate()

    def test_simple_application(self):
        import urllib.request
        contents = urllib.request.urlopen("http://localhost:8080/_/health").read()
        self.assertEquals(contents, b'OK')

    def test_simple_application_method(self):
        import urllib.request
        contents = urllib.request.urlopen("http://localhost:8080/").read()
        self.assertEquals(contents, b'Hello')

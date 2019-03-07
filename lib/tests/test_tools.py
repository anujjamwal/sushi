import unittest

from ..sushi.tools import parameter, expose


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
        self.assertEqual(params[0], dict(name="x", default=None, cls=str, method="query"))

    def test_parameter_to_raise_error_if_param_unknown(self):
        self.assertRaises(ValueError, parameter(name="y"), square)

    def test_parameter_to_store_params_in_decorator_with_type(self):
        wrapped_square = parameter(name="x", cls=int)(square)
        params = wrapped_square.params

        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], dict(name="x", default=None, cls=int, method="query"))

    def test_parameter_to_store_params_in_decorator_with_default(self):
        wrapped_square = parameter(name="x", default="y/m - c")(square)
        params = wrapped_square.params

        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], dict(name="x", default="y/m - c", cls=str, method="query"))

    def test_parameter_to_wrap_parameter_wrapped_function(self):
        wrapped_pow = parameter(name="y", cls=int)(parameter(name="x", cls=int)(pow))
        params = wrapped_pow.params

        self.assertEqual(len(params), 2)
        self.assertEqual(params[0], dict(name="x", default=None, cls=int, method="query"))
        self.assertEqual(params[1], dict(name="y", default=None, cls=int, method="query"))


class TestExpose(unittest.TestCase):

    def test_expose_without_params(self):
        w = expose(path="/")(pi)
        self.assertEquals(w.path, "/")
        self.assertEquals(w.method, "GET")
        self.assertEquals(w.params, [])
        self.assertEquals(w.func, pi)

    def test_expose_without_params_with_method(self):
        w = expose(path="/pi", method="POST")(pi)
        self.assertEquals(w.path, "/pi")
        self.assertEquals(w.method, "POST")
        self.assertEquals(w.params, [])
        self.assertEquals(w.func, pi)

    def test_expose_with_params_with_method(self):
        w = expose(path="/square")(parameter(name="x")(square))
        self.assertEquals(w.path, "/square")
        self.assertEquals(w.method, "GET")
        self.assertEquals(w.params, [dict(name="x", default=None, cls=str, method="query")])
        self.assertEquals(w.func, square)

    def test_params_with_expose(self):
        self.assertRaises(ValueError, parameter(name="y"), expose(path="/square")(square))

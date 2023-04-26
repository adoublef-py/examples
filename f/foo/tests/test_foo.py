from foo.foo import Foo
from bar.bar import bar


def test_hello_world():
    foo = Foo('World')
    assert foo.say_hello() == 'Hello World!'


def test_hello_bar():
    foo = Foo(bar)
    assert foo.say_hello() == 'Hello bar!'

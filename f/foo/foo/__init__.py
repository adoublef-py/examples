from dataclasses import dataclass


@dataclass
class Foo():
    name: str

    def say_hello(self) -> str:
        return f'Hello {self.name}!'

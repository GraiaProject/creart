from __future__ import annotations

from typing import TypeVar

from creart import AbstractCreator, add_creator, create, it
from creart.creator import CreateTargetInfo

T = TypeVar("T")


class TestCreator(AbstractCreator):
    targets = (CreateTargetInfo("builtins", "str"),)

    @staticmethod
    def create(create_type: type[T]) -> T:
        if issubclass(create_type, str):
            return "hihihi!"
        raise Exception


add_creator(TestCreator)

print(it(str))

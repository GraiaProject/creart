from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, TypeVar


@dataclass
class CreateTargetInfo:
    module: str
    identify: str
    
    # info for cli
    humanized_name: str | None = None
    description: str | None = None
    author: list[str] | None = None

T = TypeVar("T")

class AbstractCreator(metaclass=ABCMeta):
    targets: ClassVar[tuple[CreateTargetInfo, ...]]

    @staticmethod
    def available() -> bool:
        return True

    @staticmethod
    @abstractmethod
    def create(create_type: type[T]) -> T:
        ...

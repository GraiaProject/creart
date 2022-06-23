from __future__ import annotations

import os
from importlib.metadata import entry_points
from typing import Any, TypeVar

from creart.creator import AbstractCreator as AbstractCreator
from creart.creator import CreateTargetInfo as CreateTargetInfo

_created: dict[str, Any] = {}
_creators: list[type[AbstractCreator]] = []

_mapping: dict[str, type[AbstractCreator]] = {}

T = TypeVar("T")


def _env_scan():
    for entry in entry_points().get("creart.creators", []):
        creator = entry.load()
        if creator.available():
            add_creator(creator)


def add_creator(creator: type[AbstractCreator]):
    intersection = {f"{i.module}:{i.identify}" for i in creator.targets}.intersection(
        _mapping.keys()
    )
    if intersection:
        raise ValueError(f"conclict target for {', '.join(intersection)}")
    _creators.append(creator)
    _mapping.update({f"{i.module}:{i.identify}": creator for i in creator.targets})


def _signature(target: type) -> str:
    return f"{target.__module__}:{target.__name__}"


def supported(target: type):
    return _signature(target) in _mapping


def _assert_supported(target: type):
    if not supported(target):
        raise TypeError(
            f"current environment does not contain support for {_signature(target)}"
        )


def _get_creator(target: type) -> type[AbstractCreator]:
    _assert_supported(target)
    return _mapping[_signature(target)]


def create(target_type: type[T], *, cache: bool = True) -> T:
    sig = _signature(target_type)
    if cache and sig in _created:
        return _created[sig]
    _assert_supported(target_type)
    creator = _get_creator(target_type)
    result = creator.create(target_type)
    if cache:
        _created[sig] = result
    return result


it = create

if os.getenv("CREART_AUTO_SCAN") not in {"false", "False", "0", "no", "off"}:
    _env_scan()
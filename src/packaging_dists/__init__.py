from __future__ import annotations

import contextlib
import dataclasses
import re

from typing import ClassVar, Iterable, List, Optional, Tuple, Union

from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, LegacyVersion, Version

from ._utils import _extract_version_from_fragment


__all__ = [
    "__version__",
    "Distribution",
    "Sdist",
    "Wheel",
    "parse",
]

__version__ = "0.4"


AnyVersion = Union[LegacyVersion, Version]

CANONICAL_NAME_PATTERN = re.compile(
    r"^([A-Z0-9]|[A-Z0-9][A-Z0-9-]*[A-Z0-9])$", re.IGNORECASE,
)


class InvalidProject(ValueError):
    pass


class InvalidDistribution(ValueError):
    pass


class InvalidSdist(InvalidDistribution):
    pass


class InvalidWheel(InvalidDistribution):
    pass


def _split_ext(s: str, exts: Iterable[str]) -> Optional[Tuple[str, str]]:
    for ext in exts:
        if s.endswith(ext):
            end = 0 - len(ext)
            return s[:end], ext
    return "", ""


@dataclasses.dataclass()
class Sdist:
    extensions: ClassVar[List[str]] = [".tar.gz", ".zip", ".tar.bz2"]
    project: str
    version: AnyVersion

    @classmethod
    def parse(
        cls,
        filename: str,
        *,
        project: str = "",
        legacy: bool = False,
    ) -> Sdist:
        stem, ext = _split_ext(filename, cls.extensions)
        if not ext:
            raise InvalidSdist(filename)
        known_project = canonicalize_name(project)
        if known_project:
            v = _extract_version_from_fragment(stem, known_project)
            if not v:
                raise InvalidSdist(filename)
            parsed_project = known_project
        else:
            n, _, v = stem.rpartition("-")
            parsed_project = canonicalize_name(n)
        if not parsed_project:
            raise InvalidSdist(filename)
        try:
            version = Version(v)
        except InvalidVersion:
            if not legacy:
                raise InvalidSdist(filename)
            version = LegacyVersion(v)
        return cls(project=parsed_project, version=version)


@dataclasses.dataclass()
class Wheel:
    extensions: ClassVar[List[str]] = [".whl"]
    project: str
    version: Version
    build: str
    python: str
    abi: str
    platform: str

    @classmethod
    def parse(cls, filename: str, *, project: str = "") -> Wheel:
        stem, ext = _split_ext(filename, cls.extensions)
        if not ext:
            raise InvalidWheel(filename)
        try:
            n, v, *b, python, abi, platform = stem.split("-")
        except ValueError:
            raise InvalidWheel(filename)
        parsed_project = canonicalize_name(n)
        if not CANONICAL_NAME_PATTERN.match(parsed_project):
            raise InvalidWheel(filename)
        if project and parsed_project != canonicalize_name(project):
            raise InvalidWheel(filename)
        try:
            version = Version(v)
        except InvalidVersion:
            raise InvalidWheel(filename)
        if b:
            try:
                build, = b
            except ValueError:
                raise InvalidWheel(filename)
            if not build or not build[0].isdigit():
                raise InvalidWheel(filename)
        else:
            build = ""
        return cls(
            project=parsed_project,
            version=version,
            build=build,
            python=python,
            abi=abi,
            platform=platform,
        )


Distribution = Union[Sdist, Wheel]


def parse(
    filename: str,
    *,
    project: str = "",
    legacy: bool = False,
) -> Distribution:
    with contextlib.suppress(InvalidWheel):
        return Wheel.parse(filename, project=project)
    with contextlib.suppress(InvalidSdist):
        return Sdist.parse(filename, project=project, legacy=legacy)
    raise InvalidDistribution(filename)

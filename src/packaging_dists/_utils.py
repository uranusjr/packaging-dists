from packaging.utils import canonicalize_name

from typing import Optional


def _find_name_version_sep(fragment, canonical_name):
    # type: (str, str) -> int
    """Find the separator's index based on the package's canonical name.

    Copied verbatim from pip. This function is needed since the canonicalized
    name does not necessarily have the same length as the egg info's name part.
    An example::

    >>> fragment = 'foo__bar-1.0'
    >>> canonical_name = 'foo-bar'
    >>> _find_name_version_sep(fragment, canonical_name)
    8
    """
    # Project name and version must be separated by one single dash. Find all
    # occurrences of dashes; if the string in front of it matches the canonical
    # name, this is the one separating the name and version parts.
    for i, c in enumerate(fragment):
        if c != "-":
            continue
        if canonicalize_name(fragment[:i]) == canonical_name:
            return i
    raise ValueError("{} does not match {}".format(fragment, canonical_name))


def _extract_version_from_fragment(fragment, canonical_name):
    # type: (str, str) -> Optional[str]
    """Parse the version string from an sdist stem.

    This is copied verbatim from pip.
    """
    try:
        version_start = _find_name_version_sep(fragment, canonical_name) + 1
    except ValueError:
        return None
    version = fragment[version_start:]
    if not version:
        return None
    return version

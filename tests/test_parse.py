import pytest

from packaging.version import Version

from packaging_dists import Sdist, Wheel, parse


@pytest.mark.parametrize(
    "filename, expected",
    [
        # Example from PEP 427.
        (
            "distribution-1.0-1-py27-none-any.whl",
            Wheel(
                project="distribution",
                version=Version("1.0"),
                build="1",
                python="py27",
                abi="none",
                platform="any",
            ),
        ),
        # Examples from PEP 517.
        (
            "lxml-3.4.4.tar.gz",
            Sdist(project="lxml", version=Version("3.4.4")),
        ),
        (
            "mypackage-0.1.tar.gz",
            Sdist(project="mypackage", version=Version("0.1")),
        ),
        (
            "mypackage-0.1-py2.py3-none-any.whl",
            Wheel(
                project="mypackage",
                version=Version("0.1"),
                build="",
                python="py2.py3",
                abi="none",
                platform="any",
            ),
        ),
        # Some random examples.
        (
            "zope.interface-4.5.0.tar.gz",
            Sdist(project="zope-interface", version=Version("4.5.0")),
        ),
        (
            "zope.interface-4.5.0-cp36-cp36m-win_amd64.whl",
            Wheel(
                project="zope-interface",
                version=Version("4.5.0"),
                build="",
                python="cp36",
                abi="cp36m",
                platform="win_amd64",
            ),
        ),
        # tar.bz2 is a valid albeit legacy extension.
        # See https://pypi.org/project/pyahocorasick/1.1.3/#files for instance
        (
            "pyahocorasick-1.1.3.tar.bz2",
            Sdist(project="pyahocorasick", version=Version("1.1.3")),
        ),
    ],
)
def test_parse(filename, expected):
    """Examples from PEP 427.
    """
    parsed = parse(filename)
    assert parsed == expected

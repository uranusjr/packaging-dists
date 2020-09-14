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
    ],
)
def test_parse(filename, expected):
    """Examples from PEP 427.
    """
    parsed = parse(filename)
    assert parsed == expected

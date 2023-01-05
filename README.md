THE FUNCTIONALITY PROVIDED BY THIS PACKAGE HAS BEEN MERGED INTO `packaging` as
`parse_sdist_filename` AND `parse_wheel_filename`. PLEASE USE THOSE FUNCTIONS INSTEAD.

IF YOU WANT TO USE THIS LIBRARY, ADD A `packaging<22.1` REQUIREMENT TO KEEP THE CODE WORKING.


# packaging-dists

Parse distribution file names for project information. This library is not
particularly useful on its own, but can be used to make sense of distribution
information from package indexes. For example:

```pycon
>>> from packaging_dists import InvalidDistribution, parse
>>> from pypi_simple import PyPISimple
>>> client = PyPISimple()
>>> for dist in client.get_project_files("numpy"):
...     try:
...         print(parse(dist.filename))
...     except InvalidDistribution as e:
...         print(e)
(skipped)
Wheel(project='numpy', version=<Version('1.19.2')>, build='', python='cp38', abi='cp38', platform='macosx_10_9_x86_64')
Wheel(project='numpy', version=<Version('1.19.2')>, build='', python='cp38', abi='cp38', platform='manylinux1_i686')
Wheel(project='numpy', version=<Version('1.19.2')>, build='', python='cp38', abi='cp38', platform='manylinux1_x86_64')
Wheel(project='numpy', version=<Version('1.19.2')>, build='', python='cp38', abi='cp38', platform='manylinux2010_i686')
Wheel(project='numpy', version=<Version('1.19.2')>, build='', python='cp38', abi='cp38', platform='manylinux2010_x86_64')
Wheel(project='numpy', version=<Version('1.19.2')>, build='', python='cp38', abi='cp38', platform='manylinux2014_aarch64')
Wheel(project='numpy', version=<Version('1.19.2')>, build='', python='cp38', abi='cp38', platform='win32')
Wheel(project='numpy', version=<Version('1.19.2')>, build='', python='cp38', abi='cp38', platform='win_amd64')
Wheel(project='numpy', version=<Version('1.19.2')>, build='', python='pp36', abi='pypy36_pp73', platform='manylinux2010_x86_64')
Sdist(project='numpy', version=<Version('1.19.2')>)
```

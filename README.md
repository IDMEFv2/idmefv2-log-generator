# idmefv2-log-generator

This repository provides a versatile generator that can "play" (in the sense of a play list) jinja2 templates. These templates can contain either IDMEFv2 or log messages templates.

A play list is given as a yaml document, specifying the templates to "play", how they are sequenced, the rendering, etc.

## Prerequisites​

The following prerequisites must be installed on your system to install and use this library:

- Python 3.10 or later
- The Python [setuptools](https://pypi.org/project/setuptools/) package (usually available as a system package under the name `python3-setuptools`)

Python dependencies are:
- jinja2
- pyyaml
- requests
- schema

## Installation​

### Installation from sources​

It is highly recommended to install the library in a Python *virtualenv* https://virtualenv.pypa.io/en/latest/, unless running inside a container.

Installing the dependencies using `requirements.txt` is not supported; this repository provides a `pyproject.toml` which is the recommended alternative.

To install all modules, simply run in the root directory of the git clone:

``` sh
. /PATH/TO/YOUR/VIRTUALENV/bin/activate  # only if using a virtualenv
pip install --editable .
```

This will install as well the dependencies.

### Installation from packages

`idmefv2-log-generator` provides packages currently hosted on [TestPyPI](https://test.pypi.org/).

To install using TestPyPI, use the following command:

```
pip install --extra-index-url https://test.pypi.org/simple/ idmefv2-log-generator
```

## Testing​

Python unit tests using [`pytest`](https://docs.pytest.org/en/stable/) are provided:

** to be completed **

## Running

## Examples​

## Contributions​

All contributions must be licensed under the BSD license. See the LICENSE file inside this repository for more information.

To improve coordination between the various contributors, we kindly ask that new contributors subscribe to the [IDMEFv2 mailing list](https://www.freelists.org/list/idmefv2) as a way to introduce themselves.

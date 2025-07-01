# idmefv2-log-generator

This repository provides a versatile generator that can "play" (in the sense of a play list) jinja2 templates. These templates can contain either IDMEFv2 or log messages templates.

A play list is given as a yaml document, specifying the templates to "play", how they are sequenced, the rendering, etc.

## Prerequisites​

The following prerequisites must be installed on your system to install and use this library:

- Python 3.10 or later
- Python [setuptools](https://pypi.org/project/setuptools/) package (usually available as a system package under the name `python3-setuptools`)

Python dependencies are:
- jinja2
- pyyaml
- requests
- schema

## Installation​

### Installation from local sources​

It is highly recommended to install the library in a Python *virtualenv* https://virtualenv.pypa.io/en/latest/, unless running inside a container.

Installing the dependencies using `requirements.txt` is not supported; this repository provides a `pyproject.toml` which is the recommended alternative.

To install all modules, after cloning the repository, simply run in the root directory of the git clone:

``` sh
pip install --editable .
```

This will install as well the dependencies.

### Installation from github

`idmefv2-log-generator` releases can be installed directly from github repository without first cloning the repository. To install the latest release, run the following command:

``` sh
pip install git+https://github.com/IDMEFv2/idmefv2-log-generator@latest
```

It is also possible to install a specific release:

``` sh
pip install git+https://github.com/IDMEFv2/idmefv2-log-generator@V0.0.2
```

## Testing​

Python unit tests using [`pytest`](https://docs.pytest.org/en/stable/) are provided.

To run unit tests, launch:

``` sh
PYTHONPATH=... pytest -vv
```

at the root of the cloned repository, after adjusting `PYTHONPATH`.

## Play lists

### YAML play list format

A play list is defined by a YAML file.

The YAML file contains a unique `playlist` key, having the following sub-keys;
- `mode` of type str: sequential or random, defaults to sequential
- `delay` of type int: delay in seconds between each track, defaults to 0
- `repeat` of type bool: shall the playlist loop or play only once, defaults to False
- `tracks`: list of objects having the following keys:
    - `file` or `string` of type str, only one is allowed: if file, name of *template* file, else string *template*
    - `vars` of type dict: variables for template rendering, defaults to {}

An example of a playlist:

``` yaml
playlist:
    mode: random
    delay: 2
    repeat: true
    tracks:
    - file: test1.j2
    - string: "foo:{{bar}}"
        vars:
          bar: 123
```

Templates are **jinja2** templates. For more information on jinja2, refer to documentation https://jinja.palletsprojects.com/en/stable/

### Helper functions

When defining a template, helpers functions can be used:
- `now(use_utc: bool = False)`: returns current date and time in ISO 8601 format, including timezone; if `use_utc` (bool, optional) is True, the returned value will use the UTC timezone, otherwise it will use the local timezone
- `uuid()`: returns a UUID 4
- `random_ipv4(exclude_reserved: bool = False)`: returns a random IPV4 address; if `exclude_reserved` (bool, optional) is True, exclude IETF reserved address
- `random_ipv6(exclude_reserved: bool = False)`: returns a random IPV6 address; if `exclude_reserved` (bool, optional) is True, exclude IETF reserved address
- `random_string(length: int = 5)`: returns a random string of lowercase letters; `length` (int, optional) gives the length of the string and defaults to 5

An example of using helpers functions in template:

``` jinja
{% set name = random_string(10) %}
{
  "Version" : "2.D.V03",
  "ID" : "{{ uuid() }}",
  "CreateTime" : "{{ now() }}",
  "Analyzer" : {
    "IP" : "{{ random_ipv4() }}",
    "Name" : "{{ name }}",
    ... rest omitted
```

## Running

The Python package `idmefv2.generator` is directly runnable:

``` sh
python -m idmefv2.generator -h
usage: __main__.py [-h] [-t TEMPLATE_PATH] [-p PLAYER_CLASS] [--ident IDENT]
                   [--priority PRIORITY] [--url URL] [--user USER] [--password PASSWORD]
                   playlist

play a playlist defined by a .yaml file

playlist entries are jinja2 templates

playing a template means rendering it and passing the result to a player
available player Python classes are:
- PrintPlayer     a player that prints the rendered template
- RecordPlayer    a player that records the rendered template in a list
- SyslogPlayer    a player that logs the rendered template using syslog
- URLPlayer       a player that makes a HTTP POST request with JSON rendered template

positional arguments:
  playlist              yaml file defining the play list

options:
  -h, --help            show this help message and exit
  -t TEMPLATE_PATH, --template_path TEMPLATE_PATH
                        list of directories containing templates
  -p PLAYER_CLASS, --player_class PLAYER_CLASS
                        player Python class
  --ident IDENT         (SyslogPlayer only) ident, a string which is prepended to every message
  --priority PRIORITY   (SyslogPlayer only) message priority, must be one of ['emergency',
                        'alert', 'critical', 'error', 'warning', 'notice', 'info', 'debug']
  --url URL             (URLPlayer only) URL for the POST request
  --user USER           (URLPlayer only) user if URL requires authentication
  --password PASSWORD   (URLPlayer only) password if URL requires authentication
```

### Players

Playing the playlist consists of:

1. loading the templates that are defined as `file`
2. if mode is random, shuffle the tracks
3. for each track:
  - render the associated template with the variables that may be associated
  - pass the result of rendering to a *player*
4. repeat steps 2 and 3 if playlist `repeat` is True

Players are Python class that define a `play(self, rendered: str)` method which receives the result of rendering.

Available players are:
- `PrintPlayer`: a player that prints the rendered template
- `RecordPlayer`: a player that records the rendered template in a list
- `URLPlayer`: a player that makes a HTTP POST request with rendered template supposed to be JSON
- `SyslogPlayer`: a player that logs the rendered template using syslog

### Examples

An example of running the generator with a `PrintPlayer`:
``` sh
python -m idmefv2.generator -t ./examples/templates/:$HOME/tmp/templates -p PrintPlayer ./examples/list3.yaml
two
one
four
three
two
three
four
one
two
```

where `list3.yaml` contains:
``` yaml
playlist:
  mode: random
  delay: 2
  repeat: true
  tracks:
    - string: "one"
    - string: "{{number}}"
      vars:
        number: two
    - string: "three"
    - string: "{{number}}"
      vars:
        number: four
```

An example of running the generator with a `URLPlayer`:
``` sh
python -m idmefv2.generator -p URLPlayer -u http://A.B.C.D/ -U XXX -P XXX -t ./examples/templates/ ./examples/suricata1.yaml
```

An example of running the generator with a `SyslogPlayer`:
``` sh
python -m idmefv2.generator -p SyslogPlayer --ident safe4soc --priority error ./examples/list2.yaml
```

and running in parallel `tail -f /var/log/syslog` in another shell:
```sh
2025-06-05T16:32:34.351854+02:00 mimi safe4soc[344732]: one
2025-06-05T16:32:36.352554+02:00 mimi safe4soc[344732]: two
2025-06-05T16:32:38.352960+02:00 mimi safe4soc[344732]: three
2025-06-05T16:32:40.352853+02:00 mimi safe4soc[344732]: four
```

## Contributions​

All contributions must be licensed under the BSD license. See the LICENSE file inside this repository for more information.

To improve coordination between the various contributors, we kindly ask that new contributors subscribe to the [IDMEFv2 mailing list](https://www.freelists.org/list/idmefv2) as a way to introduce themselves.

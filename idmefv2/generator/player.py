'''
Module containing all players
'''
import abc
import argparse
import io
import sys
import syslog
import requests

# pylint: disable=too-few-public-methods
class Player(abc.ABC):
    '''
        Base class for players
    '''
    @abc.abstractmethod
    def play(self, rendered: str):
        '''
        Play the rendered template.
        Subclasses must implement this method.

        Args:
            rendered (str): the rendered template

        Raises:
            NotImplementedError: must be implemented in concrete sub-classes
        '''
        raise NotImplementedError

    @classmethod
    def add_argument(cls, parser: argparse.ArgumentParser = None):
        '''
        Add command line option specific to the player.
        Must call parser.add_argument() to add options.

        Args:
            parser (argparse.ArgumentParser): the argument parser
        '''

# pylint: disable=too-few-public-methods
class PrintPlayer(Player):
    '''a player that prints the rendered template'''

    def __init__(self, _: argparse.Namespace = None, out: io.TextIOBase = sys.stdout):
        self._out = out

    def play(self, rendered: str):
        print(rendered, file=self._out)

class RecordPlayer(Player, list):
    '''a player that records the rendered template in a list'''
    def __init__(self, options: argparse.Namespace = None):
        pass

    def play(self, rendered: str):
        self.append(rendered)

class URLPlayer(Player):
    '''a player that makes a HTTP POST request with JSON rendered template'''
    def __init__(self, options: argparse.Namespace):
        self._url = options.url
        self._user = options.user
        self._password = options.password

    def play(self, rendered: str):
        kwargs = {}
        kwargs['headers'] = {'Content-Type': 'application/json'}
        kwargs['data'] = rendered
        kwargs['timeout'] = 30.0
        if self._user is not None and self._password is not None:
            kwargs['auth'] = (self._user, self._password)
        # pylint: disable=missing-timeout
        r = requests.post(self._url, **kwargs)
        print(r)

    @classmethod
    def add_argument(cls, parser: argparse.ArgumentParser = None):
        parser.add_argument('--url',
                            help='(URLPlayer only) URL for the POST request',
                            dest='url')
        parser.add_argument('--user',
                            help='(URLPlayer only) user if URL requires authentication',
                            dest='user')
        parser.add_argument('--password',
                            help='(URLPlayer only) password if URL requires authentication',
                            dest='password')

class SyslogPlayer(Player):
    '''a player that logs the rendered template using syslog'''

    _PRIORITIES = {
        'emergency': syslog.LOG_EMERG,
        'alert': syslog.LOG_ALERT,
        'critical': syslog.LOG_CRIT,
        'error': syslog.LOG_ERR,
        'warning': syslog.LOG_WARNING,
        'notice': syslog.LOG_NOTICE,
        'info': syslog.LOG_INFO,
        'debug': syslog.LOG_DEBUG,
    }

    def __init__(self, options: argparse.Namespace = None):
        self._ident = options.ident
        self._priority = SyslogPlayer._PRIORITIES.get(options.priority, syslog.LOG_INFO)
        syslog.openlog(self._ident, syslog.LOG_PID)

    def play(self, rendered: str):
        syslog.syslog(self._priority, rendered)

    @classmethod
    def add_argument(cls, parser: argparse.ArgumentParser = None):
        # pylint: disable=line-too-long
        parser.add_argument('--ident',
                            help='(SyslogPlayer only) ident, a string which is prepended to every message',
                            dest='ident')
        priorities = list(SyslogPlayer._PRIORITIES.keys())
        parser.add_argument('--priority',
                            help=f"(SyslogPlayer only) message priority, must be one of {priorities}",
                            dest='priority')

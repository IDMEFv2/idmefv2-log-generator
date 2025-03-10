import abc
import argparse

# pylint: disable=too-few-public-methods
class Player(abc.ABC):
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
    def add_argument(cls, parser: argparse.ArgumentParser):
        pass

# pylint: disable=too-few-public-methods
class PrintPlayer(Player):
    '''a player that prints the rendered template'''

    def __init__(self, options: argparse.Namespace):
        pass

    def play(self, rendered: str):
        print(rendered)

class RecordPlayer(Player, list):
    '''a player that records the rendered template in a list'''
    def __init__(self, options: argparse.Namespace):
        pass

    def play(self, rendered: str):
        self.append(rendered)

class URLPlayer(Player, list):
    '''a player that makes a HTTP POST request with rendered template as JSON'''
    def __init__(self, options: argparse.Namespace):
        self._url = options.url
        self._user = options.user
        self._password = options.password

    def play(self, rendered: str):
        self.append(rendered)

    @classmethod
    def add_argument(cls, parser: argparse.ArgumentParser):
        parser.add_argument('-u', '--url',
                            help='(URLPlayer only) URL for the POST request',
                            dest='url')
        parser.add_argument('-U', '--user',
                            help='(URLPlayer only) user if URL requires authentication',
                            dest='user')
        parser.add_argument('-P', '--password',
                            help='(URLPlayer only) password if URL requires authentication',
                            dest='password')

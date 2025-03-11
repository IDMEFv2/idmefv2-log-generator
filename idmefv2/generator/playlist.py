'''
Module providing the PlayList class
'''
import io
import random
import time
import yaml
from schema import Schema, Or, Optional #, SchemaError
from jinja2 import Environment, FileSystemLoader, Template
from .player import Player
from .funs import HELPER_FUNS

# pylint: disable=too-few-public-methods
class PlayList:
    '''
    A class loading a playlist from a yaml file
    The yaml file contains a unique playlist key, having the following sub-keys;
    - mode (str): sequential or random, defaults to sequential
    - delay (int): delay between each track, defaults to 0
    - tracks: list of objects having the following keys:
      - file or string (str, exclusive): if file, name of template file, else template
      - vars (dict): variables for template rendering, defaults to {}

    Example:
    playlist:
      mode: sequential
      delay: 1
      tracks:
        - file: test1.j2
        - string: "foo:{{bar}}"
          vars:
            bar: 123

    When loading the yaml file, structure is validated using Python "schema" package
    '''
    _SCHEMA = Schema({
        'playlist': {
            Optional('mode', default='sequential'): Or('sequential', 'random'),
            Optional('delay', default=0): int,
            Optional('repeat', default=False): bool,
            'tracks': [
                {
                    Or('file','string', only_one=True): str,
                    Optional('vars', default={}): dict,
                },
            ],
        },
    })

    @classmethod
    def _validate(cls, data: dict) -> dict:
        return cls._SCHEMA.validate(data)

    def __init__(self, f : io.TextIOBase):
        y = yaml.safe_load(f)
        validated = PlayList._validate(y)
        playlist = validated['playlist']
        self._mode = playlist['mode']
        self._delay = playlist['delay']
        self._repeat = playlist['repeat']
        self._tracks = playlist['tracks']

    class _Track:
        '''
        Class storing a track of the playlist: jinja2 template and variables for rendering
        '''
        def __init__(self, template: Template, vars_dict: dict ):
            self._template = template
            self._vars = vars_dict

        def render(self) -> str:
            '''
            Renders the contained jinja2 template.

            Returns:
                str: the rendered template
            '''
            return self._template.render(self._vars)

    def _load_tracks(self, template_path: list) -> list:
        env = Environment(loader=FileSystemLoader(template_path))
        env.globals.update(HELPER_FUNS)
        tracks = []
        for t in self._tracks:
            if 'string' in t:
                template = env.from_string(t['string'])
            else:
                template = env.get_template(t['file'])
            tracks.append(self._Track(template, t['vars']))
        return tracks

    def _play_once(self, tracks: list, player: Player):
        if self._mode == 'random':
            random.shuffle(tracks)
        last = len(tracks) - 1
        for index, track in enumerate(tracks):
            player.play(track.render())
            if index < last or self._repeat:
                time.sleep(self._delay)

    def play(self, player: Player, template_path: list):
        '''
        Play the play list using the specified player.
        Loads the jinja2 templates using the specified template path.

        Args:
            player (Player): an instance of a subclass of Player
            template_path (list): list of directories where to find templates
        '''
        tracks = self._load_tracks(template_path)
        if self._repeat:
            while True:
                self._play_once(tracks, player)
        else:
            self._play_once(tracks, player)

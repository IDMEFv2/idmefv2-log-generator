import io
import random
import time
import yaml
from schema import Schema, Or, Optional #, SchemaError
from jinja2 import Environment #, FileSystemLoader
from .player import Player

class PlayList:
    _SCHEMA = Schema({
        'playlist': {
            "mode": Or('sequential', 'random'),
            'delay': int,
            Optional('repeat', default=False): bool,
            'templates': [
                {
                    Or('file','string', only_one=True): str,
                    Optional('vars'): dict,
                },
            ],
        },
    })

    @classmethod
    def _validate(cls, data: dict):
        cls._SCHEMA.validate(data)

    def __init__(self, f : io.TextIOBase):
        y = yaml.safe_load(f)
        PlayList._validate(y)
        playlist = y['playlist']
        self._mode = playlist['mode']
        self._delay = playlist['delay']
        self._repeat = playlist['repeat']
        self._templates = playlist['templates']

    def _load_templates(self):
        loaded_templates = []
        env = Environment()
        for t in self._templates:
            l = {}
            if 'vars' in t:
                l['vars'] = t['vars']
            if 'string' in t:
                l['template'] = env.from_string(t['string'])
            loaded_templates.append(l)
        return loaded_templates

    def _play_once(self, templates, player: Player):
        if self._mode == 'random':
            random.shuffle(templates)
        templates_last = len(templates) - 1
        for index, template in enumerate(templates):
            v = template['vars'] if 'vars' in template else {}
            rendered = template['template'].render(v)
            player.play(rendered)
            if index < templates_last or self._repeat:
                time.sleep(self._delay)

    def play(self, player: Player):
        loaded_templates = self._load_templates()
        if self._repeat:
            while True:
                self._play_once(loaded_templates, player)
        else:
            self._play_once(loaded_templates, player)

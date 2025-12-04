'''
Main script for the generator.
Parse command line options, load the play list and play it.
'''
import argparse
import importlib
import inspect
import json
from pathlib import Path
from .playlist import PlayList
from .player import Player

def _get_player_classes() -> dict:
    player_classes = {}
    player_module = importlib.import_module('.player', 'idmefv2.generator')
    for name in dir(player_module):
        a = getattr(player_module, name)
        if inspect.isclass(a) and not inspect.isabstract(a) and issubclass(a, Player):
            player_classes[a.__name__] = a
    return player_classes

def parse_options(players_classes: list):
    '''
    Parse command line options

    Returns:
        Namespace: parsed command line options
    '''
    description = """
play a playlist defined by a .yaml file

playlist entries are jinja2 templates

playing a template means rendering it and passing the result to a player
available player Python classes are:
"""
    for name, cls in players_classes.items():
        description += f"- {name:15} {cls.__doc__}\n"
    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('playlist', help='yaml file defining the play list')
    parser.add_argument('-t', '--template-path', help='list of directories containing templates',
                        default='', dest='template_path')
    parser.add_argument('-p', '--player-class', help='player Python class', dest='player_class')
    parser.add_argument('-d', '--dataset',
                        help='JSON dataset file applied globally to all tracks',
                        dest='dataset')
    for cls in players_classes.values():
        cls.add_argument(parser)
    return parser.parse_args()

def _load_dataset_entries(dataset_path: str | None):
    if dataset_path is None:
        return None
    path = Path(dataset_path).expanduser().resolve()
    with path.open('r', encoding='utf-8') as dataset_file:
        content = dataset_file.read()

    stripped = content.strip()
    if not stripped:
        return []

    def _validate(entries: list):
        if not isinstance(entries, list):
            raise ValueError('dataset must be a JSON array or newline-delimited JSON')
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError('dataset entries must be JSON objects')
        return entries

    try:
        parsed = json.loads(content)
        return _validate(parsed)
    except json.JSONDecodeError:
        entries = []
        for line_number, raw_line in enumerate(content.splitlines(), start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f'Invalid JSON dataset line {line_number}: {exc.msg}') from exc
        return _validate(entries)

def _main():
    players_classes = _get_player_classes()
    options = parse_options(players_classes)

    player_class = players_classes[options.player_class]
    player = player_class(options)

    template_path = options.template_path.split(':')
    playlist_path = Path(options.playlist).resolve()
    dataset_entries = _load_dataset_entries(options.dataset)
    with playlist_path.open('r', encoding="utf-8") as f:
        playlist = PlayList(f, dataset_entries=dataset_entries)
        playlist.play(player, template_path)

if __name__ == '__main__':
    _main()

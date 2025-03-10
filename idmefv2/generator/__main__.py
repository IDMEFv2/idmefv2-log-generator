import argparse
import importlib
import inspect
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
    parser.add_argument('-t', '--template_path', help='list of directories containing templates',
                        default='', dest='template_path')
    parser.add_argument('-p', '--player_class', help='player Python class', dest='player_class')
    for cls in players_classes.values():
        cls.add_argument(parser)
    return parser.parse_args()

def _main():
    players_classes = _get_player_classes()
    options = parse_options(players_classes)

    player_class = players_classes[options.player_class]
    player = player_class(options)

    template_path = options.template_path.split(':')
    with open(options.playlist, 'r', encoding="utf-8") as f:
        playlist = PlayList(f)
        playlist.play(player, template_path)

if __name__ == '__main__':
    _main()

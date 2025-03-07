import argparse
from .playlist import PlayList
from .player import PrintPlayer

def parse_options():
    '''
    Parse command line options

    Returns:
        Namespace: parsed command line options
    '''
    parser = argparse.ArgumentParser(description='Play the playlist')
    parser.add_argument('-p', '--player', help='list player', dest='player_name')
    parser.add_argument('play_list', nargs='+')
    return parser.parse_args()

def _main():
    options = parse_options()
    filename = options.play_list[0]
    with open(filename, 'r', encoding="utf-8") as f:
        play_list = PlayList(f)
    player = PrintPlayer()
    play_list.play(player)

if __name__ == '__main__':
    _main()

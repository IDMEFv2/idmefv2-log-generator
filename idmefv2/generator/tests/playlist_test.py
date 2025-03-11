# pylint: disable=missing-function-docstring
'''
Tests of PlayList
'''
import io
from idmefv2.generator.playlist import PlayList
from idmefv2.generator.player import RecordPlayer


def test_playlist1():
    yaml = '''
playlist:
  tracks:
    - string: "one"
    - string: "{{number}}"
      vars:
        number: two
    - string: "three"
    - string: "{{number}}"
      vars:
        number: four
'''
    with io.StringIO(yaml) as f:
        playlist = PlayList(f)
        player = RecordPlayer()
        playlist.play(player, '')
        assert player == ['one', 'two', 'three', 'four']

def test_playlist2():
    yaml = '''
playlist:
  mode: random
  tracks:
    - string: "A"
    - string: "{{letter}}"
      vars:
        letter: B
    - string: "C"
    - string: "{{letter}}"
      vars:
        letter: D
'''
    with io.StringIO(yaml) as f:
        playlist = PlayList(f)
        player = RecordPlayer()
        playlist.play(player, '')
        player.sort()
        assert player == ['A', 'B', 'C', 'D']

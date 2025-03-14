# pylint: disable=missing-function-docstring
'''
Tests of PlayList
'''
import io
from .playlist import PlayList
from .player import RecordPlayer, PrintPlayer

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
        playlist.play(player, [])
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
        playlist.play(player, [])
        player.sort()
        assert player == ['A', 'B', 'C', 'D']

def test_playlist3():
    yaml = '''
playlist:
  tracks:
    - string: "{{ now(True) }}"
'''
    with io.StringIO(yaml) as f, io.StringIO() as out:
        playlist = PlayList(f)
        player = PrintPlayer(out=out)
        playlist.play(player, [])
        assert out.getvalue().endswith("+00:00\n")

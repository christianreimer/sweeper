from sweeper import Game
from sweeper import Player
import io
import pytest


def test_game_1(monkeypatch, capsys):
    p = Player()
    g = Game(1, 1, p)

    monkeypatch.setattr('sys.stdin', io.StringIO('1 A'))
    g.play()
    captured = capsys.readouterr()
    assert 'Boom, you have stepped on a bomb' in captured.out


def test_game_2(monkeypatch, capsys):
    p = Player()
    g = Game(1, 0, p)

    monkeypatch.setattr('sys.stdin', io.StringIO('1 A'))
    g.play()
    captured = capsys.readouterr()
    assert 'Hurrah, you have won the game' in captured.out


def test_game_3(monkeypatch, capsys):
    p = Player()
    g = Game(1, 0, p)

    with pytest.raises(SystemExit):
        monkeypatch.setattr('sys.stdin', io.StringIO('q'))
        g.play()

    captured = capsys.readouterr()
    assert 'Goodbye ...' in captured.out

from sweeper import Player
from sweeper import Board
import io
import pytest


def test_player_1():
    p = Player()
    assert p


def test_player_2(monkeypatch):
    p = Player()
    b = Board(2, 2, None)
    monkeypatch.setattr('sys.stdin', io.StringIO('1 A'))
    x, y = p.get_move(b)
    assert (x, y) == (0, 0)


def test_player_3(monkeypatch):
    p = Player()
    b = Board(2, 2, None)
    monkeypatch.setattr('sys.stdin', io.StringIO('2 b'))
    x, y = p.get_move(b)
    assert (x, y) == (1, 1)


def test_player_4(monkeypatch):
    callback_was_called = [False]

    def quit_callback():
        callback_was_called[0] = True

    p = Player()
    b = Board(2, 2, None)
    p.goodbye = quit_callback

    monkeypatch.setattr('sys.stdin', io.StringIO('q'))
    p.get_move(b)
    assert callback_was_called


def test_player_5(monkeypatch):
    p = Player()
    b = Board(2, 2, None)

    monkeypatch.setattr('sys.stdin', io.StringIO('something not valid'))
    with pytest.raises(EOFError):
        p.get_move(b)


def test_player_6(monkeypatch):
    p = Player()
    b = Board(2, 2, None)

    monkeypatch.setattr('sys.stdin', io.StringIO('3 A'))
    with pytest.raises(EOFError):
        p.get_move(b)


def test_player_7(monkeypatch):
    callback_was_called = [False]

    def cheat_callback():
        callback_was_called[0] = True

    p = Player()
    b = Board(2, 2, None)
    p.cheat = cheat_callback

    monkeypatch.setattr('sys.stdin', io.StringIO('cheat'))
    with pytest.raises(EOFError):
        p.get_move(b)
        assert callback_was_called


from sweeper import Board
import string


def test_neighbors_special_case_1():
    suggested = Board._get_neighbors(0, 0, 1)
    assert not suggested


def test_neighbors_special_case_2():
    suggested = set(Board._get_neighbors(0, 0, 2))
    known = set(((0, 1), (1, 0), (1, 1)))
    assert suggested == known


def test_neighbors_special_case_3():
    suggested = set(Board._get_neighbors(0, 0, 3))
    known = set(((0, 1), (1, 0), (1, 1)))
    assert suggested == known


def test_neighbors_special_case_4():
    suggested = set(Board._get_neighbors(2, 0, 3))
    known = set(((1, 0), (1, 1), (2, 1)))
    assert suggested == known


def test_neighbors_normal_case():
    suggested = set(Board._get_neighbors(1, 1, 3))
    known = set(((0, 0), (0, 1), (0, 2), (1, 0), (1, 2),
                (2, 0), (2, 1), (2, 2)))
    assert suggested == known


def test_valid_move_1():
    board = Board(1, 0, None)
    assert board.valid_move(0, 0)


def test_valid_move_2():
    board = Board(1, 0, None)
    assert not board.valid_move(1, 1)


def test_valid_move_3():
    board = Board(1, 0, None)
    assert not board.valid_move(-1, 0)


def test_game_won_1():
    board = Board(0, 0, None)
    assert board.game_won()


def test_game_won_2():
    board = Board(1, 1, None)
    assert board.game_won()


def test_game_won_3():
    board = Board(1, 0, None)
    assert not board.game_won()


def test_game_won_4():
    board = Board(2, 0, None)
    for r, c in ((0, 0), (0, 1), (1, 0), (1, 1)):
        board.reveal_cell(r, c)
    assert board.game_won()


def test_game_won_5():
    board = Board(2, 0, None)
    for r, c in ((0, 1), (1, 0), (1, 1)):
        board.reveal_cell(r, c)
    assert not board.game_won()


def test_reveal_cell_1():
    callback_was_called = [False]

    def game_over_callback():
        callback_was_called[0] = True

    board = Board(1, 1, game_over_callback)
    board.reveal_cell(0, 0)
    assert callback_was_called[0]


def test_reveal_cell_2():
    callback_was_called = [False]

    def game_over_callback():
        callback_was_called[0] = True

    board = Board(1, 0, game_over_callback)
    board.reveal_cell(0, 0)
    assert not callback_was_called[0]


def test_create_board_1():
    board = Board(0, 0, None)
    assert not len(board)


def test_reveal_board_1():
    board = Board(1, 0, None)
    reveal = board.reveal_board()
    assert reveal == "  A\n1 0"


def test_reveal_board_2():
    board = Board(1, 1, None)
    reveal = board.reveal_board()
    assert reveal == "  A\n1 *"


def test_reveal_board_3():
    board = Board(2, 0, None)
    reveal = board.reveal_board()
    assert reveal == "  A B\n1 0 0\n2 0 0"


def test_show_mask_1():
    board = Board(1, 0, None)
    mask = str(board)
    assert mask == "  A\n1 %s" % Board.BLANK


def test_show_mask_2():
    board = Board(1, 1, None)
    mask = str(board)
    assert mask == "  A\n1 %s" % Board.BLANK


def test_show_mask_3():
    board = Board(2, 0, None)
    mask = str(board)
    assert mask == "  A B\n1 %s %s\n2 %s %s" % (
        Board.BLANK, Board.BLANK, Board.BLANK, Board.BLANK)


def test_valid_params_1():
    board = Board(2, 2, None)
    assert board.num_bombs == 2


def test_valid_params_2():
    board = Board(2, 5, None)
    assert board.num_bombs == 2 * 2


def test_valid_params_3():
    board = Board(100, 5, None)
    assert board.size == len(string.ascii_uppercase)

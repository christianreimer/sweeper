#! /usr/bin/env python

"""
A simple terminal version of Mine Sweeper.

Usage: sweeper.py [--size=<s>] [--bombs=<b>]

Options:
  --size=<s>   Size of the board [default: 8]
  --bombs=<b>  Number of bombs on board [default: 12]
  --help       This message
"""

import docopt
import random
import string
import sys


class Game:
    def __init__(self, size, num_bombs, player):
        self.board = Board(size, num_bombs, self.game_over)
        self.player = player
        self._set_player_hooks()
        self.continue_game = True

    def _set_player_hooks(self):
        """
        Connect the hooks so the play can exit the game (and cheat!)
        """
        self.player.goodbye = self.goodbye
        self.player.cheat = self.board.reveal_board

    def play(self):
        """
        Game loop
        """
        while self.continue_game:
            print(self.board)
            r, c = self.player.get_move(self.board)
            self.board.reveal_cell(r, c)
            if self.board.game_won():
                self.hurrah()

    def goodbye(self):
        """
        Print message and exit
        """
        print('Goodbye ...')
        sys.exit(0)

    def hurrah(self):
        """
        Print message and break out of game loop
        """
        print('Hurrah, you have won the game')
        self.continue_game = False
        print(self.board.reveal_board())

    def game_over(self):
        """
        Print message, show underlying board, and break out of game loop
        """
        print('Boom, you have stepped on a bomb')
        self.continue_game = False
        print(self.board.reveal_board())


class Board:
    """
    MineSweeper board
    """

    BOMB = '*'
    BLANK = '#'

    def __init__(self, size, num_bombs, game_over_f):
        size, num_bombs = Board._adjust_parameters(size, num_bombs)
        self.size = size
        self.num_bombs = num_bombs
        self.mask = [[Board.BLANK] * size for _ in range(size)]
        self.board = [[' '] * size for _ in range(size)]
        self.header = string.ascii_uppercase[:size]
        self.column = list(range(1, size+1))
        self.game_over = game_over_f
        self._place_bombs()
        self._place_warnings()

    def __str__(self):
        _board = []
        _board.append('  %s' % ' '.join(self.header))
        for i, row in enumerate(self.mask):
            _board.append('%s %s' % (self.column[i], ' '.join(row)))
        return '\n'.join(_board)

    def __len__(self):
        return self.size

    @staticmethod
    def _adjust_parameters(size, num_bombs):
        """
        Ensure the board is not too large, and that there are not
        more bombs than cells.
        """
        if size > len(string.ascii_uppercase):
            size = len(string.ascii_uppercase)
        if size * size < num_bombs:
            num_bombs = size * size
        return size, num_bombs

    def reveal_board(self):
        """
        Reveal the underlying board
        """
        _board = []
        _board.append('  %s' % ' '.join(self.header))
        for i, row in enumerate(self.board):
            _board.append('%s %s' % (self.column[i], ' '.join(row)))
        return '\n'.join(_board)

    def _place_bombs(self):
        """
        Please the bombs on the board in random positions
        """
        bombs_placed = 0
        possible_positions = range(self.size)
        while bombs_placed < self.num_bombs:
            r = random.choice(possible_positions) - 1
            c = random.choice(possible_positions) - 1
            if not self.board[r][c] == Board.BOMB:
                self.board[r][c] = Board.BOMB
                bombs_placed += 1

    def _place_warnings(self):
        """
        Calculate and place the warning numbers on the board
        """
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == Board.BOMB:
                    continue
                neighbors = Board._get_neighbors(r, c, self.size)
                bomb_count = str(sum([1 for (r, c) in neighbors
                                      if self.board[r][c] == Board.BOMB]))
                self.board[r][c] = bomb_count

    @staticmethod
    def _get_neighbors(r, c, size):
        """
        Return list of valid neighbors
        """
        all_possible = [(r-1, c-1), (r-1, c), (r-1, c+1),
                        (r, c-1), (r, c+1),
                        (r+1, c+1), (r+1, c), (r+1, c-1)]

        valid_possible = [(_r, _c) for _r, _c in all_possible if
                          0 <= _r < size and 0 <= _c < size]
        return valid_possible

    def valid_move(self, r, c):
        """
        Return True of this is a valid move on the current board
        """
        if r < 0 or c < 0:
            return False
        try:
            return self.mask[r][c] == Board.BLANK
        except IndexError:
            return False

    def reveal_cell(self, r, c):
        """
        Reveal a single cell on the board
        """
        assert self.valid_move(r, c)
        self.mask[r][c] = self.board[r][c]
        if self.board[r][c] == Board.BOMB:
            self.game_over()

    def game_won(self):
        """
        Check if the game has been won. The game has been won when all
        non bomb cells on the board have been revealed.
        """
        num_unrevealed = 0
        for r in self.mask:
            for c in r:
                if c == Board.BLANK:
                    num_unrevealed += 1
        return num_unrevealed == self.num_bombs


class Player:
    """
    MineSweeper Player
    """
    def __init__(self):
        self.goodbye = None
        self.cheat = None

    def get_move(self, board):
        """
        Get a move from the player and return as (r, c) 0-indexed
        coordinates
        """
        while True:
            value = input("Please enter move as ROW COL (q to quit): ")

            if value.lower() == 'q':
                self.goodbye()
                return

            if value.lower() == 'cheat':
                print(self.cheat())
                continue

            try:
                r, c = value.split()
                r = int(r) - 1  # The board uses 0 index, player uses 1
                c = board.header.find(c.upper())
                if board.valid_move(r, c):
                    return r, c
            except ValueError:
                pass


def main():  # pragma: nocover
    args = docopt.docopt(__doc__)

    size = int(args['--size'])
    bombs = int(args['--bombs'])

    p = Player()
    g = Game(size, bombs, p)
    g.play()


if __name__ == '__main__':  # pragma: nocover
    main()

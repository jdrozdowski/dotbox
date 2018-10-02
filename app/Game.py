from Board import Board
from datetime import datetime, timedelta
from random import randint


class Game:
    """
    Class Game
    """
    def __init__(self, name, width, height, players, availability):
        """
        Game class constructor.
        :param int width: Number of board's columns.
        :param int height: Number of board's rows.
        :param list players: Game players.
        :param boolean availability:
        """
        self.name = name
        self.board = Board(width, height)
        self.players = players
        self.turn = randint(0, 1)
        self.availability = availability
        self.creation_time = datetime.now()

    def assign_point(self, row, col):
        """
        Assign box's ownership and score player a point.
        :param int row: Box's row number.
        :param int col: Box's column number.
        :return boolean True:
        """
        self.board.boxes[row][col].owner = self.turn
        self.players[self.turn].score_point()

        return True

    def change_turn(self):
        """
        Change player's turn.
        :return:
        """
        if self.turn == 0:
            self.turn = 1
        elif self.turn == 1:
            self.turn = 0

    def draw_edge(self, direction, row, col):
        """
        Mark edge and check if a player scored points.
        :param string direction: Indicate type of edge (horizontal or vertical).
        :param row: Edge's row.
        :param col: Edge's column.
        :return boolean:
        """
        scored = False
        if direction == 'horizontal':
            self.board.horizontal_edges[row][col] = True
            if row < self.board.rows:
                self.board.boxes[row][col].top = True
                if self.board.boxes[row][col].is_box_complete():
                    scored = self.assign_point(row, col)
            if row > 0:
                self.board.boxes[row - 1][col].bottom = True
                if self.board.boxes[row - 1][col].is_box_complete():
                    scored = self.assign_point(row - 1, col)
        elif direction == 'vertical':
            self.board.vertical_edges[row][col] = True
            if col < self.board.cols:
                self.board.boxes[row][col].left = True
                if self.board.boxes[row][col].is_box_complete():
                    scored = self.assign_point(row, col)
            if col > 0:
                self.board.boxes[row][col - 1].right = True
                if self.board.boxes[row][col - 1].is_box_complete():
                    scored = self.assign_point(row, col - 1)

        return scored

    def is_game_over(self):
        """
        Check if a game is over.
        :return boolean:
        """
        if self.players[0].scores + self.players[1].scores == self.board.total_points:
            return True
        else:
            return False

    def is_no_players(self):
        """
        Check if there is no players in a game.
        :return boolean:
        """
        for i in range(len(self.players)):
            if self.players[i] != 'left':
                return False
        return True

    def is_time_up(self):
        """
        Check if duration of game has exceeded 30 minutes.
        :return boolean:
        """
        if datetime.now() - self.creation_time < timedelta(minutes=30):
            return False
        return True

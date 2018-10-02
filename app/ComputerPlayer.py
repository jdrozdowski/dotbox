from Player import Player
from copy import deepcopy
import random


def find_opponent_move(board):
    result = None
    move = None
    for row in range(board.rows):
        for col in range(board.cols):
            if board.boxes[row][col].count_edges() == 2:
                board_copy = deepcopy(board)
                potential_move = None
                if not board_copy.horizontal_edges[row][col]:
                    potential_move = {'direction': 'horizontal', 'row': row, 'col': col}
                    board_copy.horizontal_edges[row][col] = True
                    board_copy.boxes[row][col].top = True
                    if row - 1 >= 0:
                        board_copy.boxes[row - 1][col].bottom = True
                if not board_copy.vertical_edges[row][col + 1]:
                    if potential_move is None:
                        potential_move = {'direction': 'vertical', 'row': row, 'col': col + 1}
                    board_copy.vertical_edges[row][col + 1] = True
                    board_copy.boxes[row][col].right = True
                    if col + 1 < board_copy.cols:
                        board_copy.boxes[row][col + 1].left = True
                if board_copy.horizontal_edges[row + 1][col]:
                    if potential_move is None:
                        potential_move = {'direction': 'horizontal', 'row': row + 1, 'col': col}
                    board_copy.horizontal_edges[row + 1][col] = True
                    board_copy.boxes[row][col].bottom = True
                    if row + 1 < board_copy.rows:
                        board_copy.boxes[row + 1][col].top = True
                if not board_copy.vertical_edges[row][col]:
                    if potential_move is None:
                        potential_move = {'direction': 'vertical', 'row': row, 'col': col}
                    board_copy.vertical_edges[row][col] = True
                    board_copy.boxes[row][col].left = True
                    if col - 1 >= 0:
                        board_copy.boxes[row][col - 1].right = True

                score = close_boxes(board_copy)

                if result is None or score < result:
                    move = potential_move
                    result = score

    if move is not None:
        opponent_move = {'direction': move['direction'], 'row': move['row'], 'col': move['col']}

        return opponent_move

    return None


def close_boxes(board):
    points = 0
    for row in range(board.rows):
        for col in range(board.cols):
            if board.boxes[row][col].count_edges() == 3:
                last_line = board.boxes[row][col].find_last_edge()
                if last_line is 'top':
                    board.horizontal_edges[row][col] = True
                    board.boxes[row][col].top = True
                    if row - 1 >= 0:
                        board.boxes[row - 1][col].bottom = True
                        if board.boxes[row - 1][col].count_edges() == 4:
                            points += 1
                elif last_line is 'right':
                    board.vertical_edges[row][col + 1] = True
                    board.boxes[row][col].right = True
                    if col + 1 < board.cols:
                        board.boxes[row][col + 1].left = True
                        if board.boxes[row][col + 1].count_edges() == 4:
                            points += 1
                elif last_line is 'bottom':
                    board.horizontal_edges[row + 1][col] = True
                    board.boxes[row][col].bottom = True
                    if row + 1 < board.rows:
                        board.boxes[row + 1][col].top = True
                        if board.boxes[row + 1][col].count_edges() == 4:
                            points += 1
                elif last_line is 'left':
                    board.vertical_edges[row][col] = True
                    board.boxes[row][col].left = True
                    if col - 1 >= 0:
                        board.boxes[row][col - 1].right = True
                        if board.boxes[row][col - 1].count_edges() == 4:
                            points += 1

                points += 1

    return points


def count_points(board):
    """
    Simulate closing boxes by player and count scored points.
    :param Board instance board: Copy of game board.
    :return dictionary: Current board and scored points by player.
    """
    score = 0
    for row in range(board.rows):
        for col in range(board.cols):
            if board.boxes[row][col].count_edges() == 3:
                last_line = board.boxes[row][col].find_last_edge()
                if last_line is 'top':
                    board.horizontal_edges[row][col] = True
                    board.boxes[row][col].top = True
                    if row - 1 >= 0:
                        board.boxes[row - 1][col].bottom = True
                        if board.boxes[row - 1][col].count_edges() == 4:
                            score += 1
                elif last_line is 'right':
                    board.vertical_edges[row][col + 1] = True
                    board.boxes[row][col].right = True
                    if col + 1 < board.cols:
                        board.boxes[row][col + 1].left = True
                        if board.boxes[row][col + 1].count_edges() == 4:
                            score += 1
                elif last_line is 'bottom':
                    board.horizontal_edges[row + 1][col] = True
                    board.boxes[row][col].bottom = True
                    if row + 1 < board.rows:
                        board.boxes[row + 1][col].top = True
                        if board.boxes[row + 1][col].count_edges() == 4:
                            score += 1
                elif last_line is 'left':
                    board.vertical_edges[row][col] = True
                    board.boxes[row][col].left = True
                    if col - 1 >= 0:
                        board.boxes[row][col - 1].right = True
                        if board.boxes[row][col - 1].count_edges() == 4:
                            score += 1

                score += 1

    result = {'board': board, 'score': score}

    return result


def find_move_by_number_of_box_edges(board, number):
    """
    Find a random available edge within a box by number of box's marked edges.
    :param Board instance board: Game board.
    :param int number: Number of marked edges within a box.
    :return dictionary: CPU's move.
    """
    options = []
    for row in range(board.rows):
        for col in range(board.cols):
            if board.boxes[row][col].count_edges() == number:
                if not board.horizontal_edges[row][col]:
                    if row == 0 or board.boxes[row - 1][col].count_edges() != 2:
                        options.append({'direction': 'horizontal', 'row': row, 'col': col})
                if not board.vertical_edges[row][col + 1]:
                    if col + 1 == board.cols or board.boxes[row][col + 1].count_edges() != 2:
                        options.append({'direction': 'vertical', 'row': row, 'col': col + 1})
                if not board.horizontal_edges[row + 1][col]:
                    if row + 1 == board.rows or board.boxes[row + 1][col].count_edges() != 2:
                        options.append({'direction': 'horizontal', 'row': row + 1, 'col': col})
                if not board.vertical_edges[row][col]:
                    if col == 0 or board.boxes[row][col - 1].count_edges() != 2:
                        options.append({'direction': 'vertical', 'row': row, 'col': col})

    if options:
        return random.choice(options)
    else:
        return None


class ComputerPlayer(Player):
    """
    Class ComputerPlayer
    """
    def __init__(self):
        """
        Computer Player class constructor.
        """
        super().__init__()
        self.board_copy = None

    def find_best_move(self, board):
        """
        Find the best move in current situation.
        :param Board instance board: Game board.
        :return dictionary: CPU's move.
        """
        best_move = None

        # Find a move that enable to close a box.
        for row in range(board.rows):
            for col in range(board.cols):
                if board.boxes[row][col].count_edges() == 3:
                    last_line = board.boxes[row][col].find_last_edge()
                    if last_line is 'top':
                        best_move = {'direction': 'horizontal', 'row': row, 'col': col}
                    elif last_line is 'right':
                        best_move = {'direction': 'vertical', 'row': row, 'col': col + 1}
                    elif last_line is 'bottom':
                        best_move = {'direction': 'horizontal', 'row': row + 1, 'col': col}
                    elif last_line is 'left':
                        best_move = {'direction': 'vertical', 'row': row, 'col': col}

                    return best_move

        # Find a move that enable to draw a second edge within a box.
        best_move = find_move_by_number_of_box_edges(board, 1)

        if best_move is not None:
            return best_move

        # Find a move that enable to draw a first edge within a box.
        best_move = find_move_by_number_of_box_edges(board, 0)

        if best_move is not None:
            return best_move

        # Find a least adverse move that enable to draw a third edge within a box.
        result = None
        for row in range(board.rows):
            for col in range(board.cols):
                if board.boxes[row][col].count_edges() == 2:
                    board_copy = deepcopy(board)
                    potential_move = None
                    if not board_copy.horizontal_edges[row][col]:
                        potential_move = {'direction': 'horizontal', 'row': row, 'col': col}
                        board_copy.horizontal_edges[row][col] = True
                        board_copy.boxes[row][col].top = True
                        if row - 1 >= 0:
                            board_copy.boxes[row - 1][col].bottom = True
                    if not board_copy.vertical_edges[row][col + 1]:
                        if potential_move is None:
                            potential_move = {'direction': 'vertical', 'row': row, 'col': col + 1}
                        board_copy.vertical_edges[row][col + 1] = True
                        board_copy.boxes[row][col].right = True
                        if col + 1 < board_copy.cols:
                            board_copy.boxes[row][col + 1].left = True
                    if board_copy.horizontal_edges[row + 1][col]:
                        if potential_move is None:
                            potential_move = {'direction': 'horizontal', 'row': row + 1, 'col': col}
                        board_copy.horizontal_edges[row + 1][col] = True
                        board_copy.boxes[row][col].bottom = True
                        if row + 1 < board_copy.rows:
                            board_copy.boxes[row + 1][col].top = True
                    if not board_copy.vertical_edges[row][col]:
                        if potential_move is None:
                            potential_move = {'direction': 'vertical', 'row': row, 'col': col}
                        board_copy.vertical_edges[row][col] = True
                        board_copy.boxes[row][col].left = True
                        if col - 1 >= 0:
                            board_copy.boxes[row][col - 1].right = True

                    simulation_result = count_points(board_copy)
                    opponent_score = 1 + simulation_result['score']

                    opponent_move = find_opponent_move(simulation_result['board'])

                    if opponent_move is None:
                        my_score = 0
                    else:
                        simulation_result['board'].draw_edge(opponent_move['direction'], opponent_move['row'], opponent_move['col'])
                        simulation_result = count_points(simulation_result['board'])
                        my_score = simulation_result['score']

                    difference = my_score - opponent_score

                    if result is None or difference > result:
                        best_move = potential_move
                        result = difference

        return best_move

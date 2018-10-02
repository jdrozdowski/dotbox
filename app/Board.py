from Box import Box


class Board:
    """
    Class Board
    """
    def __init__(self, width, height):
        """
        Board class constructor.
        :param width:
        :param height:
        """
        self.cols = width
        self.rows = height
        self.total_points = width * height
        self.horizontal_edges = [[False for col in range(self.cols)] for row in range(self.rows + 1)]
        self.vertical_edges = [[False for col in range(self.cols + 1)] for row in range(self.rows)]
        self.boxes = [[Box() for col in range(self.cols)] for row in range(self.rows)]
        self.last_move = None

    def draw_edge(self, direction, row, col):
        """
        Mark edge.
        :param string direction: Indicate type of edge (horizontal or vertical).
        :param row: Edge's row.
        :param col: Edge's column.
        :return:
        """
        if direction == 'horizontal':
            self.horizontal_edges[row][col] = True
            if row < self.rows:
                self.boxes[row][col].top = True
            if row > 0:
                self.boxes[row - 1][col].bottom = True
        elif direction == 'vertical':
            self.vertical_edges[row][col] = True
            if col < self.cols:
                self.boxes[row][col].left = True
            if col > 0:
                self.boxes[row][col - 1].right = True

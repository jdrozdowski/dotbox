class Box:
    """
    Class Box
    """
    def __init__(self):
        """
        Box class constructor.
        """
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False
        self.owner = None

    def count_edges(self):
        """
        Count marked edges within a box.
        :return int:
        """
        counter = 0
        if self.top:
            counter += 1
        if self.right:
            counter += 1
        if self.bottom:
            counter += 1
        if self.left:
            counter += 1

        return counter

    def find_last_edge(self):
        """
        Find last available edge within a box.
        :return string:
        """
        if self.count_edges() == 3:
            if not self.top:
                return 'top'
            if not self.right:
                return 'right'
            if not self.bottom:
                return 'bottom'
            if not self.left:
                return 'left'
        return None

    def is_box_complete(self):
        """
        Check if a box is completed.
        :return boolean:
        """
        if self.top and self.right and self.bottom and self.left:
            return True
        else:
            return False

class Player:
    """
    Class Player
    """
    def __init__(self, player_id=None):
        """
        Player class constructor.
        :param UUID object player_id: Player's session identifier.
        """
        self.scores = 0
        self.player_id = player_id

    def get_player_id(self):
        """
        Return player's session identifier.
        :return UUID object:
        """
        return self.player_id

    def score_point(self):
        """
        Score player a point.
        :return:
        """
        self.scores += 1


class ScoreManager:
    """Object to keep track of score and lives."""

    def __init__(self, starting_lives):
        self.score = 0
        self.lives = starting_lives

    def add_points(self, points=1):
        self.score += points

    def lose_life(self):
        self.lives -= 1
        # TODO: handle game over?


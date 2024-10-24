from score import categories


class Player:
    """Player class for the Yatzy game."""
    name: str
    # scorecard for the yatzy game
    scorecard: dict[str, int | None]

    def __init__(self, name: str):
        self.name = name
        scorecard: dict[str, int | None] = {category: None for category in categories()}
        self.scorecard = scorecard

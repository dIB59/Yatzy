from dataclasses import dataclass, field


@dataclass
class Player:
    name: str
    # scorecard for the yatzy game
    scorecard: dict[str, int] = field(default_factory=lambda: {
        "Ones": None,
        "Twos": None,
        "Threes": None,
        "Fours": None,
        "Fives": None,
        "Sixes": None,
        "Three of a kind": None,
        "Four of a kind": None,
        "Full House": None,
        "Small Straight": None,
        "Large Straight": None,
        "Chance": None,
        "Yatzy": None
    })

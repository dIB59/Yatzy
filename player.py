from dataclasses import dataclass, field


@dataclass
class Player:
    name: str
    scorecard: dict = field(default_factory=dict)

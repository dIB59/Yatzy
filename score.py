def categories() -> list[str]:
    return list(category_score_map().keys())


def category_score_map() -> dict[str, callable]:
    return {
        "Ones": lambda dice: dice.count(1),
        "Twos": lambda dice: dice.count(2) * 2,
        "Threes": lambda dice: dice.count(3) * 3,
        "Fours": lambda dice: dice.count(4) * 4,
        "Fives": lambda dice: dice.count(5) * 5,
        "Sixes": lambda dice: dice.count(6) * 6,
        "Three Of A Kind": lambda dice: sum(dice) if any(dice.count(d) >= 3 for d in dice) else 0,
        "Four Of A Kind": lambda dice: sum(dice) if any(dice.count(d) >= 4 for d in dice) else 0,
        "Full House": lambda dice: 25 if any(dice.count(d) == 3 for d in dice) and any(
            dice.count(d) == 2 for d in dice) else 0,
        "Small Straight": lambda dice: 30 if {1, 2, 3, 4, 5}.issubset(set(dice)) else 0,
        "Large Straight": lambda dice: 40 if {2, 3, 4, 5, 6}.issubset(set(dice)) else 0,
        "Chance": lambda dice: sum(dice),
        "Yatzy": lambda dice: 50 if all(d == dice[0] for d in dice) and dice[0] != 0 else 0
    }


def calculate_score(category: str, dice: list[int]) -> int:
    return category_score_map().get(category, lambda dice_rolls: 0)(dice)

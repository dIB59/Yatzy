import random
from dataclasses import dataclass
from enum import Enum, auto

import input
from player import Player


def calculate_score(category: str, dice: list[int]) -> int:
    match category:
        case "Ones":
            return dice.count(1)
        case "Twos":
            return dice.count(2) * 2
        case "Threes":
            return dice.count(3) * 3
        case "Fours":
            return dice.count(4) * 4
        case "Fives":
            return dice.count(5) * 5
        case "Sixes":
            return dice.count(6) * 6
        case "Three of a kind":
            if any(dice.count(d) >= 3 for d in dice):
                return sum(dice)
            return 0
        case "Four of a kind":
            if any(dice.count(d) >= 4 for d in dice):
                return sum(dice)
            return 0
        case "Full House":
            if any(dice.count(d) == 3 for d in dice) and any(dice.count(d) == 2 for d in dice):
                return 25
            return 0
        case "Small Straight":
            if len(set(dice)) >= 4:
                return 30
            return 0
        case "Large Straight":
            if len(set(dice)) == 5:
                return 40
            return 0
        case "Chance":
            return sum(dice)
        case "Yatzy":
            if all(d == dice[0] for d in dice):
                return 50
            return 0
        case _:
            return 0


# def score_per_category(all_category: dict[str, int], dice: list[int]) -> int:
#     for category, score in all_category.items():
#         if score is None:
#             category_score = calculate_score(category, dice)
#             category[category] = category_score
#             return category_score


@dataclass
class YatzyStateMachine:

    def __init__(self, players: list[Player], max_rounds: int):
        self.current_state = self.States.START
        self.players = players
        self.current_round = 0
        self.max_rounds = max_rounds * len(players)
        self.dice = [0, 0, 0, 0, 0]
        self.re_rolls = 2

    class States(Enum):
        START = auto()
        ROLL_DICE = auto()
        SELECT_CATEGORY = auto()
        CALCULATE_SCORE = auto()
        RECORD_SCORE = auto()
        END_TURN = auto()
        GAME_OVER = auto()

    def handle_end_turn_state(self):
        self.print_current_state()
        # The game has ended
        # Print game over nicely
        if self.current_round == self.max_rounds:
            return self.States.GAME_OVER
        self.print_scorecard_as_table()
        self.current_round += 1

        return self.States.ROLL_DICE

    def print_scorecard_as_table(self):
        """Scorecard on the left column, player names on the top row."""
        # Print the table header
        header = f"{'Category':<20} " + " ".join([f"{player.name:^10}" for player in self.players])
        print()
        print(header)
        print("-" * len(header))
        # Print each category and scores for all players
        for category in self.players[0].scorecard.keys():
            row = f"{category:<20} " + " ".join(
                [f"{(player.scorecard[category] if player.scorecard[category] is not None else 'None'):^10}"
                 for player in self.players]
            )
            print(row)
        print()

    def print_current_state(self):
        print(f"Current state: {self.current_state}")

    def handle_start_state(self):
        self.print_current_state()
        # Initialize the game
        return YatzyStateMachine.States.ROLL_DICE

    def handle_roll_dice_state(self):
        self.print_current_state()
        current_player = self.players[self.current_round % len(self.players)]
        print(f"Player {current_player.name}'s turn")

        # Get the player's choice of dice to hold
        self.dice = self.roll_dice()
        self.dice.sort()

        self.print_score_for_current_roll()

        for i in range(self.re_rolls):
            print(f"You rolled: {self.dice}")
            hold_dice_index = input.get_selected_dice_index()
            print(f"Selected dice to hold: {hold_dice_index} which are:", end=" ")
            held_dice = []
            for i in hold_dice_index:
                print(self.dice[i], end=" ")
                held_dice.append(self.dice[i])
            print()

            if len(held_dice) == 5:
                return YatzyStateMachine.States.SELECT_CATEGORY

            self.dice = self.roll_dice(held_dice)
            self.dice.sort()

        return YatzyStateMachine.States.SELECT_CATEGORY

    def print_score_for_current_roll(self):
        """Prints the current player's score for all categories the current roll."""
        current_player = self.players[self.current_round % len(self.players)]
        possible_scores = {category: calculate_score(category, self.dice) for category in
                           current_player.scorecard.keys()} # improve this stupid shit, send the dict as an argument
        # print table for the current player
        print(f"{'Category':<20} {current_player.name}'s {'possible Score':<10}")
        print("-" * (38 + len(current_player.name)))
        for category, score in possible_scores.items():
            print(f"{category:<20} {score:<10}")

    def roll_dice(self, held_dice: list[int] = None):
        new_dice = []
        if held_dice is None:
            held_dice = []
        for i in range(len(self.dice) - len(held_dice)):
            new_dice.append(random.randint(1, 6))
        held_dice.extend(new_dice)
        return held_dice

    def handle_select_category_state(self):
        self.print_current_state()
        # Get the player's choice of category
        # ...
        return YatzyStateMachine.States.CALCULATE_SCORE

    def handle_calculate_score_state(self):
        self.print_current_state()
        # Calculate the score based on the chosen category and dice
        # ...
        return YatzyStateMachine.States.RECORD_SCORE

    def handle_record_score_state(self):
        self.print_current_state()

        return YatzyStateMachine.States.END_TURN

    def play(self):
        while True:
            match self.current_state:
                case YatzyStateMachine.States.START:
                    self.current_state = self.handle_start_state()
                case YatzyStateMachine.States.ROLL_DICE:
                    self.current_state = self.handle_roll_dice_state()
                case YatzyStateMachine.States.SELECT_CATEGORY:
                    self.current_state = self.handle_select_category_state()
                case YatzyStateMachine.States.CALCULATE_SCORE:
                    self.current_state = self.handle_calculate_score_state()
                case YatzyStateMachine.States.RECORD_SCORE:
                    self.current_state = self.handle_record_score_state()
                case YatzyStateMachine.States.END_TURN:
                    self.current_state = self.handle_end_turn_state()
                case YatzyStateMachine.States.GAME_OVER:
                    self.print_scorecard_as_table()
                    break

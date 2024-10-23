from dataclasses import dataclass
from enum import Enum, auto

from player import Player


@dataclass
class YatzyStateMachine:

    def __init__(self, players: list[Player], max_rounds: int):
        self.current_state = self.States.START
        self.players = players
        self.current_round = 0
        self.max_rounds = max_rounds * len(players)
        self.dice = [0, 0, 0, 0, 0]

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

        # Roll the dice
        # ...
        return YatzyStateMachine.States.SELECT_CATEGORY

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

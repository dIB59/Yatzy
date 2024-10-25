import random
from enum import Enum, auto

import input
import score
from player import Player
from score import calculate_score


class YatzyStateMachine:

    def __init__(self, players: list[Player]):
        self.current_state = self.States.START
        self.players = players
        self.current_round = 0
        self.max_rounds = len(score.categories()) * len(players) - 1
        self.dice = [0, 0, 0, 0, 0]
        self.re_rolls = 2

    class States(Enum):
        START = auto()
        ROLL_DICE = auto()
        SELECT_CATEGORY = auto()
        END_TURN = auto()
        GAME_OVER = auto()

    def handle_end_turn_state(self):
        self.print_current_state()
        # The game has ended
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
                [f"{(player.scorecard[category] if player.scorecard[category] is not None else '-'):^10}"
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
        current_player = self.get_current_player()
        print(f"Player {current_player.name}'s turn")

        # Initial dice roll
        self.dice = self.roll_dice()
        self.display_dice()

        # Player decides which dice to hold
        held_dice = self.get_held_dice()

        if len(held_dice) == len(self.dice):
            return YatzyStateMachine.States.SELECT_CATEGORY

        # Allow up to re_rolls times to hold and roll dice
        for i in range(self.re_rolls):
            self.dice = self.roll_dice(held_dice)
            self.dice.sort()
            print(f"{current_player.name} rolled: {self.dice}")
            self.print_score_for_current_roll()

            if i == self.re_rolls - 1:
                return YatzyStateMachine.States.SELECT_CATEGORY

            held_dice = self.get_held_dice()

            if len(held_dice) == len(self.dice):
                return YatzyStateMachine.States.SELECT_CATEGORY

        return YatzyStateMachine.States.SELECT_CATEGORY

    def display_dice(self):
        """Roll and sort the dice, then display the result."""
        self.dice.sort()
        print(f"{self.players[self.current_round % len(self.players)].name} rolled: {self.dice}")
        self.print_score_for_current_roll()

    def get_held_dice(self):
        """Prompt the player to select dice to hold, returning the selected dice."""
        held_dice = []
        hold_dice_index = input.get_selected_dice_index()

        if not hold_dice_index:
            print("No dice selected to hold.")
        else:
            print(f"Selected dice to hold: {hold_dice_index} which are:", end=" ")
            for i in hold_dice_index:
                if i < len(self.dice):  # Ensure the index is within bounds
                    print(self.dice[i], end=" ")
                    held_dice.append(self.dice[i])
                else:
                    print(f"\nInvalid dice index: {i}")
            print()

        return held_dice

    def print_score_for_current_roll(self):
        """Prints the current player's score for all categories the current roll."""
        current_player = self.get_current_player()
        # only prints the score which can be chosen
        possible_scores = {
            category: calculate_score(category, self.dice) if value is None else "-"
            for category, value in current_player.scorecard.items()
        }
        # improve this stupid shit, send the dict as an argument
        # print table for the current player
        print(f"{'Category':<20} {current_player.name}'s {'possible Score':<10}")
        print("-" * (38 + len(current_player.name)))

        for category, value in possible_scores.items():
            print(f"{category:<20} {value:<10}")
        print()

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
        current_player = self.get_current_player()
        chosen_category = input.get_user_category_decision(current_player)
        chosen_score = calculate_score(chosen_category, self.dice)
        current_player.scorecard[chosen_category] = chosen_score
        return YatzyStateMachine.States.END_TURN

    def get_current_player(self) -> Player:
        return self.players[self.current_round % len(self.players)]

    def handle_game_over_state(self):
        self.print_current_state()
        self.print_scorecard_as_table()

        # Find the top 3 players if possible
        # Sort the players by their total score
        sorted_players = sorted(self.players,
                                key=lambda players: sum(filter(None, players.scorecard.values())),
                                reverse=True)

        top_num_players = min(3, len(sorted_players))

        print("Game Over!")
        print(f"Top {top_num_players} players:")
        print("-" * 40)
        print(f"| Rank | Player Name         | Total Score |")
        print("-" * 40)

        for i, player in enumerate(sorted_players[:3]):
            total_score = sum(filter(None, player.scorecard.values()))
            print(f"| {i + 1:<4} | {player.name:20} | {total_score:^10} |")

        print("-" * 40)

    def play(self):
        while True:
            match self.current_state:
                case YatzyStateMachine.States.START:
                    self.current_state = self.handle_start_state()
                case YatzyStateMachine.States.ROLL_DICE:
                    self.current_state = self.handle_roll_dice_state()
                case YatzyStateMachine.States.SELECT_CATEGORY:
                    self.current_state = self.handle_select_category_state()
                case YatzyStateMachine.States.END_TURN:
                    self.current_state = self.handle_end_turn_state()
                case YatzyStateMachine.States.GAME_OVER:
                    self.handle_game_over_state()
                    break

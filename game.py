from enum import Enum, auto


class YatzyStateMachine:
    class States(Enum):
        START = auto()
        ROLL_DICE = auto()
        SELECT_CATEGORY = auto()
        CALCULATE_SCORE = auto()
        RECORD_SCORE = auto()
        END_TURN = auto()
        GAME_OVER = auto()


def next_state(state):
    match state:
        case YatzyStateMachine.States.START:
            return YatzyStateMachine.States.ROLL_DICE
        case YatzyStateMachine.States.ROLL_DICE:
            return YatzyStateMachine.States.SELECT_CATEGORY
        case YatzyStateMachine.States.SELECT_CATEGORY:
            return YatzyStateMachine.States.CALCULATE_SCORE
        case YatzyStateMachine.States.RECORD_SCORE:
            return YatzyStateMachine.States.END_TURN
        case YatzyStateMachine.States.END_TURN:
            return YatzyStateMachine.States.START
        case _:
            raise ValueError("Invalid state")


def handle_start_state(state):
    # Initialize the game
    return YatzyStateMachine.States.ROLL_DICE


def handle_roll_dice_state(state):
    # Roll the dice
    # ...
    return YatzyStateMachine.States.SELECT_CATEGORY


def handle_select_category_state(state):
    # Get the player's choice of category
    # ...
    return YatzyStateMachine.States.CALCULATE_SCORE


def handle_calculate_score_state(state):
    # Calculate the score based on the chosen category and dice
    # ...
    return YatzyStateMachine.States.RECORD_SCORE


def handle_record_score_state(state):
    # Record the score
    # ...
    return YatzyStateMachine.States.END_TURN


def handle_end_turn_state(state):
    # Check if the game is over
    # ...
    return YatzyStateMachine.States.START  # Start the next player's turn


def handle_invalid_state(state):
    raise ValueError("Invalid state")


def play_yatzy():
    state = YatzyStateMachine.States.START
    while state != YatzyStateMachine.States.GAME_OVER:
        match state:
            case YatzyStateMachine.States.START:
                state = handle_start_state(state)
            case YatzyStateMachine.States.ROLL_DICE:
                state = handle_roll_dice_state(state)
            case YatzyStateMachine.States.SELECT_CATEGORY:
                state = handle_select_category_state(state)
            case YatzyStateMachine.States.CALCULATE_SCORE:
                state = handle_calculate_score_state(state)
            case YatzyStateMachine.States.RECORD_SCORE:
                state = handle_record_score_state(state)
            case YatzyStateMachine.States.END_TURN:
                state = handle_end_turn_state(state)
            case _:
                state = handle_invalid_state(state)

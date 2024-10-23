def get_selected_dice():
    """Get user input for dice to hold and convert to list of indices."""
    hold_dice = _user_input("Enter dice to hold (1-5), separated by spaces: ", ["1", "2", "3", "4", "5", " "])
    return [int(d) - 1 for d in hold_dice.split(",") if d]


def get_num_players():
    """Get number of players for the game."""
    return int(_user_input("Enter number of players: ", [str(i) for i in range(1, 11)]))


def get_player_name():
    """Get player name for the game."""
    while True:
        name = input("Enter player name: ")
        if valid_name(name):
            return name
        print("Invalid name. Please try again.")


def _user_input(prompt: str, valid_inputs: list[str]):
    """Get user input and validate against a list of valid options."""
    while True:
        u_input = input(prompt)
        if u_input in valid_inputs:
            return u_input
        print("Invalid input. Please try again.")


def valid_name(name):
    """Check if the name is valid."""
    if len(name) > 10 or len(name) < 3:
        print("Name must be between 3 and 10 characters.")
        return False

    if name.isalpha():
        return True

    return False

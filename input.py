def get_selected_dice_index():
    """Get user input for dice to hold and convert to list of indices."""
    while True:
        user_input = input("Enter dices to hold (1-5), seperated by spaces: ")
        choices = user_input.split()
        valid_input = [str(i) for i in range(1, 6)]
        if all(choice in valid_input for choice in choices):
            return [int(choice) - 1 for choice in choices]
        print("Invalid input. Please try again.")


def get_num_players():
    """Get number of players for the game."""
    return int(_user_input("Enter number of players: ", [str(i) for i in range(1, 11)]))


def want_to_select_category():
    """Asks user if they want to select a category."""
    return _user_input("Do you want to select a category? (y/n): ", ["y", "n", "yes", "no"])


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
        u_input = u_input.lower()
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

import input
from game import YatzyStateMachine
from input import get_num_players


def main():
    num_players = get_num_players()
    player_list = list()
    for i in range(num_players):
        player_name = input.get_player_name()
        player_list.append(player_name)

    yatzy_game = YatzyStateMachine(players=player_list, max_rounds=13)

    yatzy_game.play()


if __name__ == "__main__":
    main()

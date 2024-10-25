import input
from game import YatzyStateMachine
from input import get_num_players
from player import Player


def main():
    num_players = get_num_players()
    player_list: list[Player] = list()
    for i in range(num_players):
        player_name = input.get_player_name()
        player = Player(player_name)
        player_list.append(player)

    yatzy_game = YatzyStateMachine(players=player_list)

    yatzy_game.play()


if __name__ == "__main__":
    main()

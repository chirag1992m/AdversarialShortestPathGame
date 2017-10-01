from connector.client import Client
import random


def next_edge_to_move():
    """
    Add Agent logic here
    """
    first_node = random.choice(game['graph'].keys())
    second_node = random.choice(game['graph'][first_node])
    return first_node, second_node


if __name__ == "__main__":
    client = Client('127.0.0.1', 8080, 'Chirag', 0)
    game = client.get_game()

    while True:
        start, end = next_edge_to_move()
        update = client.send_edge_move(start, end)
        print update

        if update['done']:
            break

from connector.client import Client
import random
import math


def next_edge_to_increase_cost():
    """
    Add Agent logic here
    """
    first_node = random.choice(game['graph'].keys())
    second_node = random.choice(game['graph'][first_node])
    return first_node, second_node, math.sqrt(random.randint(0, 10))


if __name__ == "__main__":
    client = Client('127.0.0.1', 8080, 'Ojas', 1)
    game = client.get_game()

    while True:
        start, end, factor = next_edge_to_increase_cost()
        update = client.send_cost_update(start, end, factor)
        print update

        if update['done']:
            break

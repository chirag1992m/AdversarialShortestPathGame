from __future__ import print_function

from core.player import Gamer
from core.graph import GraphMapState


class Game(object):
    def __init__(self, game_file):
        self.player = [Gamer(Gamer.Type.PLAYER), Gamer(Gamer.Type.ADVERSARY)]
        self.graph_map = GraphMapState.init_from_textfile(game_file)
        self.chance = 0
        self.game_running = False

    def set_players(self, players_info):
        if players_info[0]['type'] == 1:
            self.player = self.player[::-1]
            self.chance = 1
        self.player[0].set_name(players_info[0]['name'])
        self.player[1].set_name(players_info[1]['name'])

    def done(self):
        return not self.game_running

    def start_game(self):
        self.game_running = True
        self.player[self.chance].reset_timer()

    def end_game(self):
        self.game_running = False

    def make_move(self, move):
        edge, cost, done, error = self.player[self.chance].make_move(self.graph_map, move)
        if done:
            self.end_game()
        update = self.get_update(edge, cost, done, error)
        self.switch_player()

        return update

    def get_update(self, edge, cost, done, error):
        update = dict()
        update['edge'] = edge
        if self.player[self.chance].type == Gamer.Type.PLAYER:
            update['add_cost'] = cost
        else:
            update['new_cost'] = cost
        update['done'] = done
        update['error'] = error
        update['position'] = self.graph_map.current_position
        return update

    @staticmethod
    def format_update(update):
        if 'add_cost' in update:
            if update['add_cost']:
                return 'Player moved from {} to {} adding cost {}'.format(update['edge'][0],
                                                                          update['edge'][1],
                                                                          update['add_cost'])
            else:
                return 'Player made an empty movement for edge {}, {}'.format(update['edge'][0],
                                                                              update['edge'][1])
        else:
            if update['new_cost']:
                return 'Adversary made edge {}, {} cost to {}'.format(update['edge'][0],
                                                                      update['edge'][1],
                                                                      update['new_cost'])
            else:
                return 'Adversary made an empty movement for edge {}, {}'.format(update['edge'][0],
                                                                                 update['edge'][1])

    def full_state(self):
        return {
            'start_node': self.graph_map.start_node,
            'end_node': self.graph_map.end_node,
            'graph': self.graph_map.graph.adjacency_list
        }

    def switch_player(self):
        self.player[self.chance].switch_player()
        self.chance = (self.chance + 1) % 2
        self.player[self.chance].reset_timer()

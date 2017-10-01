from __future__ import print_function

from enum import Enum
import time


class Gamer(object):
    class Type(Enum):
        PLAYER = 1
        ADVERSARY = 2

        @classmethod
        def tostring(cls, val):
            for k, v in vars(cls).iteritems():
                if v == val:
                    return k

    def __init__(self, gamer_type):
        self.moves = []
        self.type = gamer_type
        self.name = Gamer.Type.tostring(self.type)
        self.player_time = None
        self.time_available = 2
        self.player_cost = 0

    def get_last_move(self):
        return self.moves[-1]

    def reset_timer(self):
        self.player_time = time.time()

    def time_left(self):
        return 2. - (time.time() - self.player_time)

    def switch_player(self):
        self.player_time = None

    def set_name(self, name):
        self.name = name
        print("Added {}: {}".format(Gamer.Type.tostring(self.type), self.name))

    def make_move(self, graph_map, move):
        if self.time_left() < 0:
            cost, edge, done, error = 0, 0, True, True
            print("Player {} ran out of time.".format(self.name))
        else:
            if self.type == Gamer.Type.PLAYER:
                edge = move['start_node'], move['end_node']
                cost, done = graph_map.move_edge(edge)
                error = False
                self.player_cost += cost

                if done:
                    print("Player ended with cost: {}".format(self.player_cost))
            else:
                edge = move['node_1'], move['node_2']
                cost_factor = move['cost_factor']
                cost = graph_map.update_edge(edge, cost_factor)
                done, error = False, False

        return edge, cost, done, error

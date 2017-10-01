import socket
import cloudpickle


class Client:
    def __init__(self, server_address, server_port, name, player_type):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server_address, server_port))

        self.send_info(name, player_type)

    def close(self):
        self.socket.close()

    def __del__(self):
        self.close()

    def send_data(self, data):
        self.socket.sendall(cloudpickle.dumps(data))

    def receive_data(self, size=1024):
        return cloudpickle.loads(self.socket.recv(size))

    def get_game(self):
        return self.receive_data(100000)

    def send_info(self, name, player_type):
        self.send_data({
            'name': name,
            'type': player_type
        })

    def send_edge_move(self, start_node, end_node):
        self.send_data({
            'start_node': start_node,
            'end_node': end_node
        })
        return self.receive_data()

    def send_cost_update(self, node_1, node_2, factor):
        self.send_data({
            'node_1': node_1,
            'node_2': node_2,
            'cost_factor': factor
        })
        return self.receive_data()

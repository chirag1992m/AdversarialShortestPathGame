# Adversarial Shortest Path Game

This is a programmatically played two player game and is 
originally intended for the study of 
[Heuristics Problem Solving](http://cs.nyu.edu/courses/fall17/CSCI-GA.2965-001/)
taught at NYU GSAS.

You can use it for any intended purpose following the 
MIT license provided.

## Description

The game involves two people/bots, namely a **Player (P)** and 
an **Adversary (A)**. The aim of P is to plan a minimum cost 
route from some source node `X` to destination node `Y` through a 
graph (max size of 1000 nodes) whose bi-directional edges have 
costs. Each time P traverses an edge, adversary A knows 
where the player is and can increase the cost of 
`any` edge e by a multiplicative factor of ``1 + sqrt(k)`` 
where k is the minimum path length (and not the cost of path) 
from either node in e to Y. Thus, in P needs to minimize it's
path cost and adversary has to maximize P's path cost.

## Things to keep in mind
- Adversary A can affect the same edge e more than once 
over several turns, each time by this factor 1 + sqrt(k). 
- All are informed of the changes and thus P has a 
chance to change the path with a lower cost.
- however if P takes the initial graph and takes the 
shortest path and that path has a single edge anywhere, 
then A might be able to make that path very expensive.
- Both A and P will be told the layout of the graph 
(which will be fixed for the entire game) 
and the source and destination nodes.
- Both A and P has a time limit of 2 seconds to make their
move or the game will run out of time and will end abruptly.
- If P or A makes a move involving an edge or position which
does not exist or cannot be traversed or the cost factor by 
adversary is wrong, their move will silently be ignored.
- Cost of every edge initially is 1.0

## Platform Requirement
- Python >= 2.7
- [cloudpickle](https://github.com/cloudpipe/cloudpickle)

## How to run Game Server
To run the game with default options:
```commandline
cd /path/to/AdversarialShortestPathGame
python -m game
```
This will start the game server on the port 8080 loading
the default game file given in [sample](sample/advshort.txt).
And, finally wait for the client bots to connect to the 
server. A maximum of two bots will connect where one will
act as the adversary and the other as the player.

**Note:** the game will only run after both the bots are
connected.

To see all the available options run:
```commandline
cd /path/to/AdversarialShortestPathGame
python -m game -h
```

## Run game bots
Random strategy based game bots are given the [sample](sample)
directory, namely [Player](sample/test_client_player.py) and
[Adversary](sample/test_client_adversarial.py) which connect
to the game server and randomly makes move based on the 
current game layout.

To run the sample clients:
```commandline
cd /path/to/AdversarialShortestPathGame
python -m sample.test_client_player


# In New terminal
cd /path/to/AdversarialShortestPathGame
python -m sample.test_client_adversary
```
Order of connection does not matter, but, if both the bots are 
players or both the bots are adversary, the game behavior is 
undefined.

## Make your own bots
You can directly edit the client bots given in the 
[sample](sample) directory and run them as usual. There
is a comment line `Add Agent Logic here` where you can make 
your changes based on the updates and the game layout.

Also, you can see the available options in the bit clients
by adding the argument `-h` while running.

## Communication between server-client
The communication is based on simple key-value based 
dictionary which is serialized using cloudpickle for 
transfer over the sockets.

Initially, after you construct the client with the required
arguments, you get the game layout using client.get_game()
which gives you a dictionary of the format:
```python
{
    'start_node': X,
    'end_node': Y,
    'graph': dict(list(nodes)) # Adjacency Lists of the graph
}
```

After a move by the Player P, an update is received of the
format:
```python
{
    'done': True/False, # If the game has ended or not
    'edge': (node_1, node_2), # The last edge moved
    'error': True/False, # If the player ran out of time
    'position': Player_position, # The current position of the player P
    'add_cost': cost # Cost added by the players move. It will be 0 if the player didn't move any edge
}
```

After a move by the Adversary A, an update is received of the
format:
```python
{
    'done': True/False, # is the game complete?
    'edge': (node_1, node_2), # The edge affected
    'error': True/False, # Did the Adversary ran out of time?
    'position': Player_position, # The current position of the player which is obviously unchanged from the last update
    'new_cost': cost # New cost of the edge. If it is 0, the edge given doesn't exist or the cost factor given didn't confer to 1 + sqrt(k) rule
}
```

## Future Architecture Teams for Graph based games
I have helpful guidance waiting for you [here](GraphBasedGamesArchitecture.md).
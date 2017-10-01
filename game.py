from core.game_looper import GameLooper

if __name__ == "__main__":
    port = 8080
    address = ''
    game_file = 'sample/advshort.txt'

    game = GameLooper(address, port, game_file)
    game.run_game_loop()

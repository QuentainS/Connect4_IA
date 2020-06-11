import pickle


class Game():
    def __init__(self, width, height):
        # Setup the size of the game
        self.width = width
        self.height = height
        self.used_discs = 0

        # Init the game with all cases to 0
        self.map = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def get_map(self):
        return (self.width, self.height, self.map)

    def set_disc(self, player, coord):
        x = coord[0]
        y = coord[1]
        y = self.height - y - 1

        # Check if the case is empty
        if self.map[y][x] != 0:
            raise Exception("Case not empty")

        # Check if the move is feasible
        # (if the case below the target is not empty)
        if y != (self.height - 1) and self.map[y+1][x] == 0:
            raise Exception("Your disc can't levitate...")

        self.map[y][x] = player

        self.used_discs += 1

        # Check if this a is a win-move
        # TODO

        if self.is_tie():
            return -1
        return 0

    def is_tie(self):
        return self.used_discs == self.width * self.height


class Match():
    def __init__(self, width, height):
        self.game = Game(width, height)

        self.turn = 0

        # 0 if no winner
        # 1 or 2 if there is a winner
        # -1 if this is tie
        self.winner = 0

        self.states = [self.get_state()]

    def play(self, player, coord):

        if (self.turn % 2) + 1 != player:
            print("It is the turn of player {}!".format((self.turn % 2) + 1))
        else:

            print("Player n°{} add a disc on {}".format(player, coord))

            # Add the disc
            try:
                self.winner = self.game.set_disc(player, coord)
            except Exception as e:
                raise e

            if self.winner != 0:
                if self.winner == player:
                    print("Player {} won".format(self.winner))
                elif self.winner == -1:
                    print("This is a tie...")

            self.turn += 1
            self.states.append(self.get_state())

    def get_state(self):
        return {'map': self.game.get_map(), 'turn': self.turn, 'winner': self.winner}

    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.states, f)

    def show(self):
        width, height, game_map = self.game.get_map()
        for y in range(height):
            for x in range(width):
                print(game_map[y][x], end=' ')
            print('\n')

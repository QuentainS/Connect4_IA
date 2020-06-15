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
        elif x < 0 or x >= self.width:
            raise Exception("Wrong index : x={} is not correct".format(x))
        elif y < 0 or y >= self.height:
            raise Exception("Wrong index : y={} is not correct".format(y))

        # Check if the move is feasible
        # (if the case below the target is not empty)
        if y != (self.height - 1) and self.map[y+1][x] == 0:
            raise Exception("Your disc can't levitate...")

        self.map[y][x] = player

        self.used_discs += 1

        # Check if this a is a win-move
        if self.is_win_move(x, y, player):
            return player
        elif self.is_tie():
            return -1
        return 0

    def is_win_move(self, x, y, player):

        # Get the amount of discs (of this player)
        # on the left
        left = 0
        i = x - 1
        while i >= 0 and self.map[y][i] == player:
            left += 1
            i -= 1

        # on the right
        right = 0
        i = x + 1
        while i < self.width and self.map[y][i] == player:
            right += 1
            i += 1

        # down
        down = 0
        j = y + 1
        while j < self.height and self.map[j][x] == player:
            down += 1
            j += 1

        # up-left diagonal
        up_left = 0
        i = x - 1
        j = y - 1
        while i >= 0 and j >= 0 and self.map[j][i] == player:
            up_left += 1
            i -= 1
            j -= 1

        # up-right diagonal
        up_right = 0
        i = x + 1
        j = y - 1
        while i < self.width and j >= 0 and self.map[j][i] == player:
            up_right += 1
            i += 1
            j -= 1

        # down-left diagonal
        down_left = 0
        i = x - 1
        j = y + 1
        while i >= 0 and j < self.height and self.map[j][i] == player:
            down_left += 1
            i -= 1
            j += 1

        # down-right diagonal
        down_right = 0
        i = x + 1
        j = y + 1
        while i < self.width and j < self.height and self.map[j][i] == player:
            down_right += 1
            i += 1
            j += 1

        horizontal = left + right
        diagonal_1 = up_left + down_right
        diagonal_2 = up_right + down_left

        # If 3 adjacents disk => Connect 4 !
        return horizontal == 3 or down == 3 or diagonal_1 == 3 or diagonal_2 == 3

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

        if self.winner != 0:
            raise Exception("Game already finished")
        elif (self.turn % 2) + 1 != player:
            raise Exception("Bad player")
        else:
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

    def get_all_states(self):
        return self.states

    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.states, f)

    def get_turn(self):
        return self.turn

    def show(self):
        width, height, game_map = self.game.get_map()
        for y in range(height):
            for x in range(width):
                print(game_map[y][x], end=' ')
            print('\n')

    def is_finished(self):
        return self.winner != 0

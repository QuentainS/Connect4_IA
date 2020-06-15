import socket
import ast


class Client():
    def __init__(self, pseudo, ip='127.0.0.1', port=1233):
        self.ClientSocket = socket.socket()
        self.host = ip
        self.port = port
        self.pseudo = pseudo
        self.conn_state = 0
        self.player_number = 0

    def get_player_number(self):
        return self.player_number

    def connect(self):
        print('[+] Connecting to the server')
        try:
            self.ClientSocket.connect((self.host, self.port))
            self.conn_state = 1
            self.send_message(self.pseudo)
        except socket.error as e:
            print(str(e))
        print("[+] Connected !")

    def disconnect(self):
        self.ClientSocket.close()

    def wait_player_number(self):

        print("[+] Wait the player number...")

        data = self.ClientSocket.recv(1024)
        data = data.decode()

        if "PLAYER" in data:
            self.player_number = int(data[6:])
            print("[+] Your are the player n°{}".format(self.player_number))

    def wait_state(self):
        print("[+] Getting the state...")

        data = self.ClientSocket.recv(1024)
        data = data.decode()

        if "STATE" in data:
            state = data[5:]
            self.game_state = ast.literal_eval(state)

        elif "QUIT" in data:
            print("[X] Connection closed by the server")
            self.conn_state = 0

        elif "ERR" in data:
            player = data[3]
            error = data[4:]
            print("[X] Player {} made an error : {}".format(player, error))
            self.conn_state = 0

        else:
            pass

    def is_my_turn(self):
        return self.player_number == (self.game_state['turn'] % 2) + 1

    def is_connected(self):
        return self.conn_state

    def send_message(self, message):
        self.ClientSocket.sendall(message.encode())

    def get_winner(self):
        return self.game_state['winner']

    def show_game(self):
        width, height, game_map = self.game_state['map']
        for y in range(height):
            for x in range(width):
                print(game_map[y][x], end=' ')
            print('\n')


# Create the client with a pseudo
client = Client("Zeblood")
client.connect()

while client.get_player_number() == 0:
    client.wait_player_number()

# While the client if connected
while client.is_connected():

    # Receive the state
    client.wait_state()

    # Check if the game is over
    winner = client.get_winner()
    if winner != 0:
        client.show_game()
        if winner == 0:
            print("[+] This is a tie !")
        else:
            print("[+] Player {} won the game !".format(winner))
        break

    # If an error occured, we are disconnected
    if not client.is_connected():
        break

    client.show_game()

    # If it's not my turn
    if not client.is_my_turn():
        pass

    # Otherwise, compute and send the order
    else:
        print("[?] Your order : ")
        order = input()
        client.send_message(order)

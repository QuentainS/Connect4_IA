import socket
import os
import random
import time
from connect4 import Match, Game
from datetime import datetime
import pickle


class Server():
    def __init__(self, ip='127.0.0.1', port=3545):
        self.ServerSocket = socket.socket()
        self.host = ip
        self.port = port
        self.clients = []
        self.history = []

    def open(self):
        try:
            self.ServerSocket.bind((self.host, self.port))
        except socket.error as e:
            print(str(e))
        self.ServerSocket.listen(5)

    def close(self):
        srv.send_to_clients("QUIT")
        self.ServerSocket.close()

    def err_close(self, error):
        # Send the error and the player who did it
        current_player = (self.match.get_turn() % 2) + 1
        srv.send_to_clients("ERR{}{}".format(current_player, error))
        self.ServerSocket.close()

    def wait_a_player(self):

        # Wait the first player
        print("[+] Waiting for a player... {}/2".format(len(self.clients)))
        client, address = self.ServerSocket.accept()

        # Get its pseudo
        pseudo = client.recv(1024).decode()
        print('[!] {} is connected from {}:{}'.format(
            pseudo, address[0], address[1]))

        # Add it to the clients list
        self.clients.append({'pseudo': pseudo, 'conn': client})

    def init_match(self):

        # Randomly choose the 1st and the 2nd player
        random.shuffle(self.clients)

        # Create the match
        self.match = Match(6, 7)

        # Announce the player order to each one
        self.clients[0]['conn'].sendall("PLAYER1".encode())
        self.clients[1]['conn'].sendall("PLAYER2".encode())

    def send_state(self):
        state = "STATE"
        state += str(self.match.get_state())

        self.send_to_clients(state)

    def send_to_clients(self, message):
        for client in self.clients:
            client['conn'].sendall(message.encode())

    def wait_a_play(self):

        # Check the turn value of the match to know who have to play
        current_player = self.match.get_turn() % 2

        # print("Waiting order from player {} ({})".format(
        #    current_player+1, self.clients[current_player]['pseudo']))

        order = self.clients[current_player]['conn'].recv(1024)
        order = order.decode()
        print("[+] Order received from player {}: {}".format(current_player + 1, order))

        pos = int(order)

        # Try to apply the move
        try:
            self.match.play(current_player+1, pos)
        except Exception as e:
            raise e

        self.history.append(self.match.get_state())

    def match_finished(self):
        return self.match.is_finished()

    def save_game(self):
        name_file = datetime.now().strftime('save/server_%H_%M_%S_%d_%m_%Y.pkl')
        pickle.dump(self.history, open(name_file, "wb"))
        print("[+] Game saved to {}".format(name_file))


# Create the server an open the connection
srv = Server()
srv.open()

# Wait the two players
srv.wait_a_player()
srv.wait_a_player()

# Create the match and define the player order
srv.init_match()

time.sleep(1)
# Send the current state and wait for a play
while not srv.match_finished():

    # Sending the current state to each clients
    srv.send_state()

    # Get the order an play it
    try:
        srv.wait_a_play()
    # In case of error, close the connection an send the error to the clients
    except Exception as e:
        print("[!] Error from player : {}".format(e))
        srv.err_close(e)
        break

# If no error
if srv.match_finished():
    # Send the last state
    srv.send_state()
    # Close the connection
    srv.close()
    # Save the game
    srv.save_game()

import os
import socket
import pickle

SERVER_IP = os.getenv("CHECKERS_SERVER_IP", "127.0.0.1")
PORT = 5555

class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER_IP
        self.port = PORT
        self.addr = (self.server, self.port)
        self.color = self.connect()

    def connect(self) -> str:
        """Connects to the server and returns the assigned player color."""
        try:
            self.client.connect(self.addr)
            data = pickle.loads(self.client.recv(2048))
            return data["color"]
        except Exception as e:
            print(f"Network Connection Error: {e}")
            return "Offline"

    def send(self, data: dict) -> dict:
        """Sends a dictionary to the server and returns the server's response."""
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(16384))
        except socket.error as e:
            print(f"Socket Error: {e}")
            return {}
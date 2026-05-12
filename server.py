import socket
import threading
import pickle
import checkers as ck

SERVER_IP = "0.0.0.0"  # Accept connections on all network interfaces
PORT = 5555
MAX_PLAYERS = 2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    raise

s.listen(MAX_PLAYERS)
local_ip = socket.gethostbyname(socket.gethostname())
print(f"Server Started. Waiting for connections on 0.0.0.0:{PORT} (LAN IP: {local_ip})")

# Initialize the shared board once both players are connected
initial_board = ck.Checkers().board

game_state = {
    "board": None,
    "current_player": "White",
    "ready": False
}

connections = []
player_colors = ["White", "Black"]
player_count = 0

def threaded_client(conn: socket.socket, player_color: str):
    global player_count
    
    # Send the client their assigned color on connection
    conn.send(pickle.dumps({"color": player_color}))
    
    while True:
        try:
            # Wait for requests from the client
            data = pickle.loads(conn.recv(16384))
            
            if not data:
                break
                
            if data["type"] == "GET":
                # Client is just asking for the latest board state
                conn.send(pickle.dumps(game_state))
                
            elif data["type"] == "UPDATE":
                # Client made a move and pushed a new board state
                game_state["board"] = data["board"]
                game_state["current_player"] = data["current_player"]
                conn.send(pickle.dumps(game_state))
                
        except Exception as e:
            break

    print(f"Lost connection with {player_color}")
    connections.remove(conn)
    conn.close()
    player_count -= 1
    
    if player_count < 2:
        game_state["ready"] = False
        game_state["board"] = None
        game_state["current_player"] = "White"

while True:
    conn, addr = s.accept()
    print(f"Connected to: {addr}")
    
    if player_count >= MAX_PLAYERS:
        conn.send(pickle.dumps({"error": "Server full"}))
        conn.close()
        print(f"Rejected connection from {addr}: server full")
        continue

    connections.append(conn)
    color = player_colors[player_count % 2]

    if len(connections) == MAX_PLAYERS:
        game_state["ready"] = True
        if game_state["board"] is None:
            game_state["board"] = initial_board
        print("Both players connected. Game is ready.")

    threading.Thread(target=threaded_client, args=(conn, color), daemon=True).start()
    player_count += 1

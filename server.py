import socket
import threading
import pickle

SERVER_IP = "127.0.0.1"
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Server Started. Waiting for connections...")

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
    connections.append(conn)
    print(f"Connected to: {addr}")
    
    color = player_colors[player_count % 2]
    
    if len(connections) == 2:
        game_state["ready"] = True
        
    threading.Thread(target=threaded_client, args=(conn, color)).start()
    player_count += 1
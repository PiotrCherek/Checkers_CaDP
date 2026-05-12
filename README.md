# Checkers: Concurrent & Distributed Processing

Implementation of the classic board game Checkers. This project was developed to explore and demonstrate the complexities of **distributed systems**, **client-server synchronization**, and **concurrent thread management** using Python.

---

## Game Description
**Key Gameplay Features:**
* **Standard Ruleset:** Includes diagonal movement, king piece promotion, and mandatory captures.
* **Multi-Capture Logic:** Supports complex jump sequences in a single turn.
* **Networked Play:** Real-time interaction between two distinct client instances.
---

## Project File Structure
The project follows a modular architecture to separate concerns between networking, game logic, and UI.

| File | Role | Description |
| :--- | :--- | :--- |
| `server.py` | **The Orchestrator** | Manages incoming socket connections and broadcasts the global game state. |
| `network.py` | **The Bridge** | Handles the low-level socket communication and data transmission logic. |
| `main.py` | **The Entry Point** | Initializes the Pygame window and runs the client-side event loop. |
| `game.py` | **State Manager** | Tracks the board array, current turn and move validation. |
| `checkers.py` | **Game Engine** | Contains the move logic and drawing. |

---

## Concurrent Programming Methods
To handle multiple players without lag or state corruption, the following techniques were used:

* **Multi-threading**
* **Socket Programming** 
* **Object Serialization**
* **Atomic Updates** 

---

## External Libraries & Frameworks
* **[Pygame](https://www.pygame.org/):** 
* **Standard Python Libraries:**
    * `socket`: For low-level networking.
    * `threading`: For concurrent execution.

---

## Screenshots of the game

<img width="1731" height="826" alt="image" src="https://github.com/user-attachments/assets/d247fa4e-4cc8-4bcc-8c25-41388f557f2b" />
<img width="1729" height="825" alt="image" src="https://github.com/user-attachments/assets/81fc8ccd-fa35-42b7-a78f-2af00f4bf750" />

---

## Group Members & Contributions
| Member | Responsibilities |
| :--- | :--- |
| **Mateusz** | King promotion and advanced game rules, communication protocols bettwen processes|
| **Kacper** | Pawns movement and basic game rules, client implementation |
| **Piotrek** | Board logic and UI, server implementation |

---

## Installation & Launch
1.  **Install Pygame:**
    ```bash
    pip install pygame
    ```
2.  **Run the Server:**
    ```bash
    python server.py
    ```
3.  **Run two Clients:**
    ```bash
    python main.py
    ```

import requests
import chess
import chess.svg
import svgwrite

# --- CONFIGURATION ---
USERNAME = "YOUR_USERNAME"  # Replace with your Chess.com or Lichess username
SOURCE = "chess.com"  # Options: "chess.com" or "lichess"
OUTPUT_FILE = "chess-board.svg"

def fetch_latest_game():
    """Fetch the latest completed chess game."""
    if SOURCE == "chess.com":
        url = f"https://api.chess.com/pub/player/{USERNAME}/games/archives"
        response = requests.get(url).json()
        last_month_url = response["archives"][-1]  # Get latest month archive
        games = requests.get(last_month_url).json()["games"]
        last_game = games[-1] if games else None
    elif SOURCE == "lichess":
        url = f"https://lichess.org/api/games/user/{USERNAME}?max=1&moves=true&format=json"
        response = requests.get(url).json()
        last_game = response[0] if response else None
    else:
        raise ValueError("Invalid source. Use 'chess.com' or 'lichess'.")

    return last_game

def generate_svg_board(fen):
    """Generate an SVG chessboard based on a FEN position."""
    board = chess.Board(fen)
    svg_data = chess.svg.board(board=board, size=500)
    with open(OUTPUT_FILE, "w") as f:
        f.write(svg_data)

def main():
    game = fetch_latest_game()
    if not game:
        print("No recent games found.")
        return

    if SOURCE == "chess.com":
        fen = game.get("fen", "startpos")
    elif SOURCE == "lichess":
        fen = game["moves"][-1]["fen"] if "moves" in game else "startpos"

    generate_svg_board(fen)
    print(f"Chessboard updated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

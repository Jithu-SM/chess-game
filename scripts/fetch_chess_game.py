import requests
import chess
import chess.svg

# --- CONFIGURATION ---
USERNAME = "itsXIGIE"  # Replace with your actual Chess.com or Lichess username
SOURCE = "chess.com"  # Options: "chess.com" or "lichess"
OUTPUT_FILE = "chess-board.svg"

def fetch_latest_game():
    """Fetch the latest completed chess game."""
    try:
        if SOURCE == "chess.com":
            url = f"https://api.chess.com/pub/player/{USERNAME}/games/archives"
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Error fetching data: {response.status_code}")
                print(f"Response: {response.text}")
                return None
            
            data = response.json()
            if "archives" not in data:
                print("Error: No archives found.")
                return None

            last_month_url = data["archives"][-1]
            games = requests.get(last_month_url).json().get("games", [])
            if not games:
                print("Error: No games found in last archive.")
                return None
            
            last_game = games[-1]
        
        elif SOURCE == "lichess":
            url = f"https://lichess.org/api/games/user/{USERNAME}?max=1&moves=true&format=json"
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Error fetching data: {response.status_code}")
                print(f"Response: {response.text}")
                return None

            games = response.json()
            if not games:
                print("Error: No games found for Lichess.")
                return None
            
            last_game = games[0]
        else:
            raise ValueError("Invalid source. Use 'chess.com' or 'lichess'.")

        return last_game

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def generate_svg_board(fen):
    """Generate an SVG chessboard based on a FEN position."""
    board = chess.Board(fen)
    svg_data = chess.svg.board(board=board, size=500)
    with open(OUTPUT_FILE, "w") as f:
        f.write(svg_data)

def main():
    game = fetch_latest_game()
    if not game:
        print("No recent games found. Exiting.")
        return

    fen = game.get("fen", "startpos") if SOURCE == "chess.com" else game.get("moves", [{}])[-1].get("fen", "startpos")
    
    if fen == "startpos":
        print("Error: No FEN position found.")
        return

    generate_svg_board(fen)
    print(f"✅ Chessboard updated: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()


"Rock-Paper-Scissors-Plus Game Referee"

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import random

load_dotenv()

game_state = {
    "round": 1,
    "player_score": 0,
    "computer_score": 0,
    "player_bomb_used": False,
    "computer_bomb_used": False,
    "game_over": False
}

# functions for game logic
def determine_winner(p1: str, p2: str) -> str:
    """Returns 'player', 'computer', or 'draw'"""
    if p1 == p2:
        return "draw"
    if p1 == "bomb":
        return "player"
    if p2 == "bomb":
        return "computer"
    wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    return "player" if wins[p1] == p2 else "computer"


def computer_choice() -> str:
    """Computer picks a move with 20% bomb chance if available"""
    if not game_state["computer_bomb_used"] and random.random() < 0.2:
        return "bomb"
    return random.choice(["rock", "paper", "scissors"])


def play_round(move: str) -> str:
    """Play one round with the given player move"""
    global game_state
    
    if game_state["game_over"]:
        return "Game over! Type 'reset' to play again."
    
    move = move.lower().strip()
    valid = ["rock", "paper", "scissors", "bomb"]
    
    if move not in valid:
        return f"Invalid move '{move}'! Choose: rock, paper, scissors, or bomb."
    
    if move == "bomb" and game_state["player_bomb_used"]:
        return "You already used your bomb! Choose rock, paper, or scissors."
    
    if move == "bomb":
        game_state["player_bomb_used"] = True
    
    comp = computer_choice()
    if comp == "bomb":
        game_state["computer_bomb_used"] = True
    
    result = determine_winner(move, comp)
    
    if result == "player":
        game_state["player_score"] += 1
        outcome = "You win!"
    elif result == "computer":
        game_state["computer_score"] += 1
        outcome = "Computer wins!"
    else:
        outcome = "Draw!"
    
    r = game_state["round"]
    ps = game_state["player_score"]
    cs = game_state["computer_score"]
    
    response = f"Round {r}: You={move}, Computer={comp}. {outcome} Score: {ps}-{cs}"
    
    game_state["round"] += 1
    if ps >= 2 or cs >= 2 or game_state["round"] > 3:
        game_state["game_over"] = True
        if ps > cs:
            response += " 🎉 YOU WIN THE GAME!"
        elif cs > ps:
            response += " 🤖 Computer wins the game!"
        else:
            response += " 🤝 It's a tie!"
        response += " Type 'reset' for new game."
    
    return response


def get_status() -> str:
    """Get current game status"""
    r = game_state["round"]
    ps = game_state["player_score"]
    cs = game_state["computer_score"]
    bomb = "yes" if not game_state["player_bomb_used"] else "no"
    over = "yes" if game_state["game_over"] else "no"
    return f"Round: {r}, Score: You {ps} - {cs} Computer, Bomb available: {bomb}, Game over: {over}"


def reset_game() -> str:
    """Reset game state for a new game"""
    global game_state
    game_state = {
        "round": 1,
        "player_score": 0,
        "computer_score": 0,
        "player_bomb_used": False,
        "computer_bomb_used": False,
        "game_over": False
    }
    return "New game started! Make your move: rock, paper, scissors, or bomb."


# Agent
root_agent = Agent(
    name="rps_plus_referee",
    model=LiteLlm(model="groq/llama-3.1-70b-versatile"),
    description="Rock-Paper-Scissors-Plus Game Referee",
    instruction="""You host a Rock-Paper-Scissors-Plus game.

Rules: Best of 3. Moves: rock, paper, scissors, bomb. Bomb beats all but only once per game.

When user says hi/hello: Welcome them and explain the rules briefly, then ask for their move.

When user says rock/paper/scissors/bomb: Call play_round with their move, then tell them the result.

When user says reset/new game: Call reset_game, then confirm the new game started.

When user asks score/status: Call get_status, then tell them the score.

Only call ONE tool per user message. After the tool returns, summarize the result naturally.""",
    tools=[play_round, get_status, reset_game],
)

# Rock-Paper-Scissors Game Referee

# Game Rules

• Objective: Best of 3 rounds wins the game
• Moves: rock, paper, scissors, bomb
• Standard Rules: Rock beats scissors, scissors beats paper, paper beats rock
• Special Rule: Bomb beats everything (but each player can only use it once!)

# Quick Start

1- Install Dependencies
   pip install google-adk litellm python-dotenv

2- Environment setup
   Create `.env` file:

3- Run the Game
   adk web

4- Play
   Say "hi" to see rules
   Make moves: "rock", "paper", "scissors", "bomb"
   Check score: "status"
   New game: "reset"


# Features
• Persistent game state across conversation turns
• Best-of-3 scoring with automatic game completion
• Bomb mechanics (beats all moves, once per game)
• Real-time score tracking


# Examples
User: hi
Bot: Welcome to Rock-Paper-Scissors-Plus!
     Rules: Best of 3. Moves: rock, paper, scissors, bomb...

User: rock
Bot: Round 1: You=rock, Computer=scissors. You win! Score: 1-0

User: bomb
Bot: Round 2: You=bomb, Computer=paper. You win! Score: 2-0
     YOU WIN THE GAME! Type 'reset' for new game.

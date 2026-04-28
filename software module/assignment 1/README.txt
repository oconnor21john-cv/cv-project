TRIVIA QUIZ APPLICATION - README

Author: John
Date: November 2025

CONTENTS
1. Overview
2. Features
3. How to Use
4. Error Handling
5. Questions
6. Technical Info

1. OVERVIEW
This is a trivia quiz program written in Python that runs in Python IDLE.
Multiple people can take the quiz and it keeps track of everyone's scores.
There are 15 trivia questions and you can choose how many you want to answer.

The questions come up in random order each time and you get feedback on your
answers. It also shows a leaderboard at the end if more than one person plays.


2. FEATURES AND FUNCTIONALITY


BASIC FEATURES:

- 15 trivia questions with correct answers
- User name input and validation
- Running score tracking during the quiz
- Final score display (X out of 10 format)
- Percentage score calculation
- Multiple user support - as many users as you want can take the quiz
- Leaderboard showing all users' scores
- Highest scorer identification (handles ties)
- Average score calculation across all users

EXTRA FEATURES:

- Customizable number of questions (1-15 questions)
- Random question ordering - questions appear in different order each time
- Detailed feedback showing:
  - Which questions were answered correctly
  - Which questions were answered incorrectly
  - The correct answer for incorrect questions
  - Interesting explanations for each answer
- Comprehensive input validation and error handling
- User-friendly interface with formatting
- Performance messages based on score
- Graceful handling of program interruption (Ctrl+C)

3. HOW TO USE THE QUIZ SYSTEM

STEP-BY-STEP WALKTHROUGH:

Step 1: Starting the Program
   - Run quiz_application.py in Python IDLE (press F5)
   - You'll see a welcome screen with the quiz title and features

Step 2: Customizing the Quiz (Optional)
   - The program asks: "Would you like to choose the number of questions?"
   - Type "yes" or "no" and press Enter
   - If yes: Enter a number between 1 and 15
   - If no: The quiz will default to 10 questions

Step 3: Entering Your Name
   - When prompted, enter your name
   - Names must:
     * Not be empty
     * Contain at least one letter
   - Press Enter to continue

Step 4: Answering Questions
   - Read each question carefully
   - Type your answer and press Enter
   - Answers are NOT case-sensitive (e.g., "Dogs" = "dogs" = "DOGS")
   - You'll immediately see if your answer is correct or incorrect
   - Your running score is tracked throughout

Step 5: Viewing Your Results
   - After all questions, you'll see:
     * Your name
     * Your score (e.g., 7/10)
     * Your percentage (e.g., 70%)
     * A performance message
   - Detailed breakdown showing:
     * Each question you answered
     * Your answer vs. the correct answer
     * Explanations for interesting facts

Step 6: Adding More Users
   - The program asks: "Does anybody else want to take the quiz?"
   - Type "yes" if another person wants to play
   - Type "no" if you're done
   - Each new user goes through Steps 3-5

Step 7: Final Statistics
   - After all users finish, you'll see:
     * Complete leaderboard (ranked by score)
     * The highest scorer(s)
     * Average score of all participants
     * Total number of participants

Step 8: Exiting
   - The program displays a goodbye message and exits automatically
   - You can also press Ctrl+C at any time to exit early

4. INPUT VALIDATION AND ERROR HANDLING

The program includes robust error handling for various scenarios:

NAME INPUT:
X Empty name → Error: "Name cannot be empty. Please try again."
X Only spaces → Error: "Name cannot be empty. Please try again."
X Only numbers (e.g., "123") → Error: "Name must contain at least one letter."
- Valid: "John", "Mary Smith", "Alex123", etc.

YES/NO QUESTIONS:
X Invalid input → Error: "Please enter 'yes' or 'no'."
- Valid: "yes", "y", "no", "n" (case-insensitive)

NUMBER INPUT (Question Count):
X Empty input → Error: "Please enter a number between 1 and 15."
X Not a number → Error: "Please enter a valid number."
X Out of range → Error: "Number must be between 1 and 15."
- Valid: Any number from 1 to 15

ANSWER INPUT:
X Empty answer → Error: "Answer cannot be empty. Please provide an answer."
- Valid: Any non-empty text (case-insensitive matching)

SPECIAL CASES:
- Ctrl+C (Program Interruption) → Gracefully exits with a goodbye message
- Unexpected Errors → Caught and displayed with helpful message

5. QUESTION BANK INFORMATION


QUESTION TYPES:

- Multiple choice questions (choose a, b, c, or d)
- Text answer questions (type your answer)
- Multiple acceptable answers (e.g., Henry VIII question accepts "three" or "3")

ANSWER MATCHING:

- Case-insensitive (Dogs = dogs = DOGS)
- Exact match required (but trimmed of extra spaces)
- For text questions, type the word or number
- Multiple acceptable answers supported (e.g., "three" or "3")


6. TECHNICAL DETAILS

FILE STRUCTURE:
quiz_application.py (main program file)
README.txt (this file)

PROGRAMMING CONCEPTS USED:

- Functions: Modular design with 11 separate functions
- Data Structures: Lists, Dictionaries, Tuples
- Conditional Statements: if/elif/else for logic and validation
- Iterative Statements: for loops, while loops
- Type Hints: Modern Python type annotations
- Error Handling: try/except blocks
- List Comprehensions: Efficient data processing
- Lambda Functions: Sorting operations
- Random Module: Question shuffling

KEY FUNCTIONS:

1. get_quiz_questions() - Returns the question bank
2. get_valid_name() - Validates and returns user name
3. get_valid_yes_no() - Validates yes/no responses
4. get_valid_number() - Validates numeric input
5. get_answer() - Gets quiz answer from user
6. check_answer() - Validates if answer is correct
7. run_quiz() - Executes the quiz for one user
8. display_results() - Shows individual user results
9. display_statistics() - Shows overall statistics
10. main() - Orchestrates the entire program

DATA STRUCTURES:

Questions: List of dictionaries
  [{
    "question": str,
    "answer": str or list,
    "explanation": str
  }]

Results: List of dictionaries
  [{
    "name": str,
    "score": int,
    "total": int,
    "percentage": float
  }]

CODE COMMENTS:

The source code includes:
- Module-level docstring explaining the program
- Function docstrings with descriptions, parameters, and return values
- Inline comments explaining complex logic
- Section headers organizing the code
- Type hints for better code clarity

DEMO/PRESENTATION TIPS

When demonstrating this system, show:

1. USER INTERFACE:
   - Clean welcome screen
   - Clear prompts and instructions
   - Formatted output
   - Clear feedback messages

2. BASIC FUNCTIONALITY:
   - Enter a name and take the full quiz
   - Show score calculation
   - Add multiple users
   - Display final leaderboard

3. EXTRA FEATURES:
   - Customize number of questions
   - Show questions appear in random order (run quiz twice)
   - Point out detailed feedback with explanations
   - Show correct answer display for wrong answers

4. ERROR HANDLING:
   - Try empty name → shows error
   - Try name with only numbers → shows error
   - Try empty answer → shows error
   - Try invalid yes/no response → shows error
   - Try out-of-range number → shows error
   - Show Ctrl+C graceful exit

5. SOURCE CODE HIGHLIGHTS:
   - Show modular function design
   - Point out comprehensive comments
   - Highlight input validation functions
   - Show use of data structures (lists, dictionaries)



END OF README



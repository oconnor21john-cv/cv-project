"""
Quiz Application
Author: John
Date: November 2025

A trivia quiz program that lets multiple users take a quiz with random questions.
Keeps track of scores and shows statistics at the end.
"""

import random
from typing import List, Dict, Tuple


# questions
def get_quiz_questions():
    """
    Get all the quiz questions
    Returns a list of question dictionaries with options and answers
    """
    questions = [
        {
            "question": "The Canary Islands are named after which animal?",
            "options": {
                "a": "Canaries",
                "b": "Dogs",
                "c": "Cats",
                "d": "Horses"
            },
            "answer": "b",
            "explanation": "Despite the name, they're named after dogs (Latin: canis), not canaries!"
        },
        {
            "question": "Which is the longest month of the year?",
            "options": {
                "a": "December",
                "b": "July",
                "c": "October",
                "d": "January"
            },
            "answer": "c",
            "explanation": "October is 31 days plus has an extra hour when clocks go back, making it an hour longer!"
        },
        {
            "question": "What is Michael J. Fox's middle name?",
            "options": {
                "a": "James",
                "b": "John",
                "c": "Andrew",
                "d": "Joseph"
            },
            "answer": "c",
            "explanation": "The 'J' stands for Andrew. He added it as a stage name!"
        },
        {
            "question": "What is Paul McCartney's middle name?",
            "options": {
                "a": "John",
                "b": "Paul",
                "c": "George",
                "d": "Richard"
            },
            "answer": "b",
            "explanation": "His full name is James Paul McCartney, so Paul is actually his middle name!"
        },
        {
            "question": "Which famous artist designed the Chupa Chups logo?",
            "options": {
                "a": "Pablo Picasso",
                "b": "Salvador Dali",
                "c": "Andy Warhol",
                "d": "Joan Miró"
            },
            "answer": "b",
            "explanation": "The surrealist artist Salvador Dalí designed this iconic lollipop logo in 1969!"
        },
        {
            "question": "What company makes the most number of tyres in a year?",
            "options": {
                "a": "Michelin",
                "b": "Goodyear",
                "c": "Bridgestone",
                "d": "LEGO"
            },
            "answer": "d",
            "explanation": "LEGO produces more tyres than any other company, though they're miniature!"
        },
        {
            "question": "Which of these is one of the four Pac-Man ghosts?",
            "options": {
                "a": "Blinky",
                "b": "Slinky",
                "c": "Dinky",
                "d": "Winky"
            },
            "answer": "a",
            "explanation": "The four ghosts are Pinky, Inky, Blinky, and Clyde!"
        },
        {
            "question": "France shares its longest land border with which country?",
            "options": {
                "a": "Spain",
                "b": "Germany",
                "c": "Brazil",
                "d": "Italy"
            },
            "answer": "c",
            "explanation": "French Guiana (considered part of France) shares a long border with Brazil!"
        },
        {
            "question": "Dump, floater, and wipe are terms used in which team sport?",
            "options": {
                "a": "Basketball",
                "b": "Volleyball",
                "c": "Soccer",
                "d": "Tennis"
            },
            "answer": "b",
            "explanation": "These are all techniques used in volleyball!"
        },
        {
            "question": "A human has 7 neck vertebrae. How many does a giraffe have?",
            "options": {
                "a": "14",
                "b": "21",
                "c": "7",
                "d": "10"
            },
            "answer": "c",
            "explanation": "Despite their long necks, giraffes also have 7 vertebrae, just like humans!"
        },
        {
            "question": "What is the most common British pub name?",
            "options": {
                "a": "The Crown",
                "b": "The Red Lion",
                "c": "The King's Head",
                "d": "The White Hart"
            },
            "answer": "b",
            "explanation": "The Red Lion is the most common pub name in Britain!"
        },
        {
            "question": "What's the biggest animal in the world?",
            "options": {
                "a": "African Elephant",
                "b": "Blue Whale",
                "c": "Giraffe",
                "d": "Great White Shark"
            },
            "answer": "b",
            "explanation": "The blue whale is the largest animal ever known to have lived on Earth!"
        },
        {
            "question": "How many of Henry VIII's wives were called Catherine?",
            "answer": ["three", "3"],
            "type": "text",
            "explanation": "Three of his wives were named Catherine: Catherine of Aragon, Catherine Howard, and Catherine Parr!"
        },
        {
            "question": "What colour is found on 75% of the world's flags?",
            "answer": "red",
            "type": "text",
            "explanation": "Red appears on approximately 75% of all national flags around the world!"
        },
        {
            "question": "Which animal's milk is used in pecorino cheese?",
            "options": {
                "a": "Cow",
                "b": "Goat",
                "c": "Sheep",
                "d": "Buffalo"
            },
            "answer": "c",
            "explanation": "Pecorino is an Italian cheese made from sheep's milk!"
        }
    ]
    
    return questions


# validation stuff
def get_valid_name():
    """Get user's name with validation"""
    while True:
        name = input("\nPlease enter your name: ")
        name = name.strip()
        
        if name == "":
            print("Error: Name cannot be empty. Please try again.")
            continue
        
        # check name has at least one letter
        has_letter = False
        for char in name:
            if char.isalpha():
                has_letter = True
                break
        
        if not has_letter:
            print("Error: Name must contain at least one letter. Please try again.")
            continue
        
        return name


def get_valid_yes_no(prompt):
    """Ask a yes/no question and validate the answer"""
    while True:
        response = input(f"\n{prompt} (yes/no): ")
        response = response.strip()
        response = response.lower()
        
        if response == 'yes' or response == 'y':
            return True
        elif response == 'no' or response == 'n':
            return False
        else:
            print("Error: Please enter 'yes' or 'no'.")


def get_valid_number(prompt, min_val, max_val):
    """Get a number from user within a specific range"""
    valid_input = False
    while not valid_input:
        try:
            value = input(f"\n{prompt} ({min_val}-{max_val}): ")
            value = value.strip()
            
            if value == "":
                print(f"Error: Please enter a number between {min_val} and {max_val}.")
                continue
            
            num = int(value)
            
            # check range
            if num < min_val:
                print(f"Error: Number must be between {min_val} and {max_val}.")
                continue
            if num > max_val:
                print(f"Error: Number must be between {min_val} and {max_val}.")
                continue
            
            valid_input = True
            return num
            
        except ValueError:
            print("Error: Please enter a valid number.")


def get_answer(question_num, total_questions):
    """Get the user's answer for a quiz question"""
    valid_answer = False
    while not valid_answer:
        answer = input(f"\nYour answer (a/b/c/d) [{question_num}/{total_questions}]: ")
        answer = answer.strip()
        answer = answer.lower()
        
        if answer == "":
            print("Error: Answer cannot be empty. Please enter a, b, c, or d.")
            continue
        
        # check if valid option
        if answer == 'a' or answer == 'b' or answer == 'c' or answer == 'd':
            valid_answer = True
            return answer
        else:
            print("Error: Please enter a valid option: a, b, c, or d.")


# checking answers
def check_answer(user_answer, correct_answer):
    """Check if the user's answer is correct"""
    # convert to lowercase and remove spaces
    user_ans = user_answer.lower()
    user_ans = user_ans.strip()
    
    # check if correct_answer is a list (multiple acceptable answers)
    if type(correct_answer) == list:
        # check against each possible answer
        for possible_answer in correct_answer:
            correct_ans = possible_answer.lower()
            correct_ans = correct_ans.strip()
            if user_ans == correct_ans:
                return True
        return False
    else:
        # single answer
        correct_ans = correct_answer.lower()
        correct_ans = correct_ans.strip()
        
        if user_ans == correct_ans:
            return True
        else:
            return False


def run_quiz(questions, num_questions):
    """Run the quiz for a single user"""
    # pick random questions from the list
    total_available = len(questions)
    if num_questions > total_available:
        num_to_select = total_available
    else:
        num_to_select = num_questions
    
    selected_questions = random.sample(questions, num_to_select)
    
    score = 0
    results = []
    
    print("\nQUIZ STARTED! Good luck!\n")
    
    # loop through questions
    question_number = 0
    for q in selected_questions:
        question_number = question_number + 1
        
        print()
        print(f"Question {question_number} of {num_questions}:")
        print(f"  {q['question']}")
        print()
        
        # check what type of question
        question_type = q.get('type')
        if question_type == 'text':
            # text answer question
            user_answer = input(f"\nYour answer [{question_number}/{num_questions}]: ")
            user_answer = user_answer.strip()
            is_correct = check_answer(user_answer, q['answer'])
            
            if is_correct == True:
                print("Correct!")
                score = score + 1
            else:
                print("Incorrect!")
            
            # store result
            result_dict = {}
            result_dict['question'] = q['question']
            result_dict['user_answer'] = user_answer
            result_dict['user_answer_text'] = user_answer
            
            # handle list or string answer
            if type(q['answer']) == list:
                result_dict['correct_answer'] = q['answer'][0]
                result_dict['correct_answer_text'] = ' or '.join(q['answer'])
            else:
                result_dict['correct_answer'] = q['answer']
                result_dict['correct_answer_text'] = q['answer']
            
            result_dict['is_correct'] = is_correct
            if 'explanation' in q:
                result_dict['explanation'] = q['explanation']
            else:
                result_dict['explanation'] = ''
            result_dict['options'] = None
            results.append(result_dict)
        else:
            # multiple choice
            options = q['options']
            letters = ['a', 'b', 'c', 'd']
            for letter in letters:
                print(f"    {letter}) {options[letter]}")
            
            user_answer = get_answer(question_number, num_questions)
            
            # check if correct
            is_correct = check_answer(user_answer, q['answer'])
            
            if is_correct == True:
                print("Correct!")
                score = score + 1
            else:
                print("Incorrect!")
            
            # store the result
            result_dict = {}
            result_dict['question'] = q['question']
            result_dict['user_answer'] = user_answer
            result_dict['user_answer_text'] = options[user_answer]
            result_dict['correct_answer'] = q['answer']
            result_dict['correct_answer_text'] = options[q['answer']]
            result_dict['is_correct'] = is_correct
            if 'explanation' in q:
                result_dict['explanation'] = q['explanation']
            else:
                result_dict['explanation'] = ''
            result_dict['options'] = options
            results.append(result_dict)
    
    return score, results


def display_results(name, score, total, results, show_details=True):
    """Display the results for a user"""
    # calculate percentage
    percentage = (score / total) * 100
    
    print("\nQUIZ RESULTS")
    print(f"Name: {name}")
    print(f"Score: {score}/{total}")
    print(f"Percentage: {percentage:.1f}%")
    
    # give feedback based on score
    if percentage >= 90:
        print("Outstanding! You're a trivia master!")
    elif percentage >= 70:
        print("Great job! Well done!")
    elif percentage >= 50:
        print("Good effort! Keep learning!")
    elif percentage < 50:
        print("Keep trying! Practice makes perfect!")
    
    if show_details == True:
        print("\nDETAILED BREAKDOWN:")
        
        # loop through all results
        result_num = 0
        for result in results:
            result_num = result_num + 1
            
            if result['is_correct'] == True:
                status = "[CORRECT]"
            else:
                status = "[INCORRECT]"
            
            print(f"\n{result_num}. {result['question']}")
            
            # check type
            if result['options'] == None:
                # text question
                print(f"   Your answer: {result['user_answer']}")
                if result['is_correct'] == False:
                    print(f"   Correct answer: {result['correct_answer']}")
                    if result['explanation'] != '':
                        print(f"   Note: {result['explanation']}")
            else:
                # multiple choice
                print(f"   Your answer: {result['user_answer']}) {result['user_answer_text']}")
                if result['is_correct'] == False:
                    print(f"   Correct answer: {result['correct_answer']}) {result['correct_answer_text']}")
                    if result['explanation'] != '':
                        print(f"   Note: {result['explanation']}")


def display_statistics(all_results):
    """Show statistics for all users"""
    if len(all_results) == 0:
        return
    
    print("\nFINAL STATISTICS\n")
    
    # sort results by score (highest first)
    sorted_results = []
    for result in all_results:
        sorted_results.append(result)
    
    # bubble sort
    n = len(sorted_results)
    for i in range(n):
        for j in range(0, n-i-1):
            if sorted_results[j]['score'] < sorted_results[j+1]['score']:
                temp = sorted_results[j]
                sorted_results[j] = sorted_results[j+1]
                sorted_results[j+1] = temp
    
    print("LEADERBOARD:")
    position = 0
    for result in sorted_results:
        position = position + 1
        print(f"{position}. {result['name']}: {result['score']}/{result['total']} "
              f"({result['percentage']:.1f}%)")
    
    # find who got highest score
    highest_score = sorted_results[0]['score']
    highest_scorers = []
    for r in sorted_results:
        if r['score'] == highest_score:
            highest_scorers.append(r['name'])
    
    print()
    num_winners = len(highest_scorers)
    if num_winners == 1:
        print(f"Highest Score: {highest_scorers[0]} with {highest_score} points!")
    else:
        winner_names = ', '.join(highest_scorers)
        print(f"Highest Score (Tie): {winner_names} with {highest_score} points!")
    
    # calculate average score
    total_score = 0
    for r in all_results:
        total_score = total_score + r['score']
    
    num_users = len(all_results)
    avg_score = total_score / num_users
    avg_total = all_results[0]['total']
    avg_percentage = (avg_score / avg_total) * 100
    
    print(f"Average Score: {avg_score:.1f}/{avg_total} ({avg_percentage:.1f}%)")
    
    total_participants = len(all_results)
    print(f"Total Participants: {total_participants}")


# main function
def main():
    """Main function to run the quiz"""
    print("\nTRIVIA QUIZ GAME\n")
    print("Welcome to the Trivia Quiz!")
    print("Test your knowledge with fascinating questions on various topics.")
    print("\nFeatures:")
    print("  - Random question ordering")
    print("  - Customizable number of questions")
    print("  - Detailed feedback and explanations")
    print("  - Score tracking and leaderboard\n")
    
    all_questions = get_quiz_questions()
    max_questions = len(all_questions)
    
    # ask if they want to pick number of questions
    customize = get_valid_yes_no("Would you like to choose the number of questions?")
    
    if customize == True:
        num_questions = get_valid_number(
            f"How many questions would you like to answer?",
            1, max_questions
        )
    else:
        num_questions = 10
    
    print(f"\nQuiz set to {num_questions} questions.")
    
    all_results = []
    
    # main loop
    keep_going = True
    while keep_going:
        user_name = get_valid_name()
        print(f"\nWelcome, {user_name}! Let's begin your quiz.")
        
        score, results = run_quiz(all_questions, num_questions)
        
        # work out percentage
        percentage = (score / num_questions) * 100
        
        # save results
        user_result = {}
        user_result['name'] = user_name
        user_result['score'] = score
        user_result['total'] = num_questions
        user_result['percentage'] = percentage
        all_results.append(user_result)
        
        display_results(user_name, score, num_questions, results, show_details=True)
        
    
        another_user = get_valid_yes_no("Does anybody else want to take the quiz?")
        
        if another_user == False:
            keep_going = False
    
    # show final stats if multiple people played
    num_users = len(all_results)
    if num_users > 1:
        display_statistics(all_results)
    
    print("\nThank you for playing the Trivia Quiz!")
    print("Hope you learned something new today!\n")


# Run the program
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please restart the program.")


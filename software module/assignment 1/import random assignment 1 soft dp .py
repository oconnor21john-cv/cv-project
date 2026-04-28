import random

# Quiz application for assignment 1
# John - November 2025

class QuizQuestion:
    # class to store quiz questions and answers
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer.lower().strip()  # make lowercase and remove spaces
    
    def check_answer(self, user_answer):
        # check if the answer is correct
        # convert to lowercase and remove whitespace for comparison
        user_ans = user_answer.lower().strip()
        if user_ans == self.answer:
            return True
        else:
            return False
    
    def __str__(self):
        return f"Q: {self.question} | A: {self.answer}"


class QuizTaker:
    # this class keeps track of each person taking the quiz
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.answers = []  # stores tuples of (question, user_answer, is_correct)
    
    def add_answer(self, question, user_answer, is_correct):
        # add the answer to the list and update score
        self.answers.append((question, user_answer, is_correct))
        if is_correct:
            self.score = self.score + 1
    
    def get_percentage(self, total_questions):
        # calculate the percentage score
        if total_questions > 0:
            percentage = (self.score / total_questions) * 100
            return percentage
        else:
            return 0


class QuizSystem:
    # Main class for the quiz system
    def __init__(self):
        self.questions = []
        self.quiz_takers = []
        self.total_questions = 0
    
    def setup_quiz(self):
        # setup the quiz questions
        print("=== QUIZ SETUP ===")
        print("Setting up general knowledge quiz...")
        
        # 10 general knowledge questions
        default_questions = [
            ("What is the capital of France?", "Paris"),
            ("How many continents are there?", "7"),
            ("What is the largest planet in our solar system?", "Jupiter"),
            ("Who wrote 'Romeo and Juliet'?", "William Shakespeare"),
            ("What is the chemical symbol for gold?", "Au"),
            ("How many days are in a leap year?", "366"),
            ("What is the smallest prime number?", "2"),
            ("What is the main language spoken in Brazil?", "Portuguese"),
            ("How many bones are in the human body?", "206"),
            ("What is the fastest land animal?", "Cheetah")
        ]
        
        # add each question to the questions list
        for q, a in default_questions:
            new_question = QuizQuestion(q, a)
            self.questions.append(new_question)
        
        self.total_questions = len(self.questions)
        print(f"Quiz setup complete! {self.total_questions} questions loaded.")
    
    def get_user_name(self):
        # get the user's name and make sure it's not empty
        while True:
            name = input("Please enter your name: ")
            name = name.strip()
            if name != "":
                return name
            else:
                print("Error: Name cannot be empty. Please try again.")
    
    def take_quiz(self, user):
        # this function runs the actual quiz
        print(f"\n=== QUIZ START ===")
        print(f"Good luck, {user.name}! Answer the following questions:")
        
        # shuffle the questions so they're in random order
        shuffled_questions = self.questions.copy()
        random.shuffle(shuffled_questions)
        
        question_num = 1
        for question in shuffled_questions:
            print(f"\nQuestion {question_num}/{self.total_questions}:")
            print(f"{question.question}")
            
            # get the user's answer (make sure they enter something)
            while True:
                user_answer = input("Your answer: ")
                user_answer = user_answer.strip()
                if user_answer != "":
                    break
                else:
                    print("Error: Answer cannot be empty. Please try again.")
            
            # check if answer is correct
            is_correct = question.check_answer(user_answer)
            user.add_answer(question, user_answer, is_correct)
            
            # give feedback
            if is_correct:
                print("Correct!")
            else:
                print("Incorrect!")
            
            question_num += 1
    
    def show_individual_results(self, user):
        # show the results for one user
        print(f"\n=== RESULTS FOR {user.name.upper()} ===")
        print(f"Final Score: {user.score}/{self.total_questions}")
        percentage = user.get_percentage(self.total_questions)
        print(f"Percentage: {percentage:.1f}%")
        
        print(f"\n=== DETAILED FEEDBACK ===")
        counter = 1
        for question, user_answer, is_correct in user.answers:
            print(f"\nQuestion {counter}: {question.question}")
            print(f"Your answer: {user_answer}")
            print(f"Correct answer: {question.answer}")
            if is_correct:
                print(f"Status: CORRECT")
            else:
                print(f"Status: INCORRECT")
            counter += 1
    
    def show_overall_statistics(self):
        # display statistics for all users who took the quiz
        if len(self.quiz_takers) == 0:
            print("No quiz results available yet.")
            return
        
        print("\n=== OVERALL STATISTICS ===")
        
        # find who got the highest score
        highest_scorer = self.quiz_takers[0]
        for user in self.quiz_takers:
            if user.score > highest_scorer.score:
                highest_scorer = user
        
        print(f"HIGHEST SCORE: {highest_scorer.name} - {highest_scorer.score}/{self.total_questions} ({highest_scorer.get_percentage(self.total_questions):.1f}%)")
        
        # show all the scores
        print(f"\nALL SCORES:")
        for user in self.quiz_takers:
            perc = user.get_percentage(self.total_questions)
            print(f"- {user.name}: {user.score}/{self.total_questions} ({perc:.1f}%)")
        
        # calculate the average score
        total_score = 0
        for user in self.quiz_takers:
            total_score = total_score + user.score
        
        average_score = total_score / len(self.quiz_takers)
        average_percentage = (average_score / self.total_questions) * 100
        
        print(f"\nAVERAGE SCORE: {average_score:.1f}/{self.total_questions} ({average_percentage:.1f}%)")
    
    def reset_quiz_data(self):
        # clear all the quiz taker data
        self.quiz_takers = []
        print("All user data has been reset!")
    
    def run(self):
        # main function that runs the program
        print("\n" * 3)
        print("=== WELCOME TO THE QUIZ SYSTEM ===")
        
        # setup the quiz
        self.setup_quiz()
        
        # main menu loop
        while True:
            print("\n=== MAIN MENU ===")
            print("1. Take Quiz")
            print("2. View Statistics")
            print("3. Reset Quiz Data")
            print("4. Exit")
            
            choice = input("Choose an option (1-4): ")
            choice = choice.strip()
            
            if choice == "1":
                self.handle_quiz_session()
            elif choice == "2":
                print("\n" * 2)
                self.show_overall_statistics()
            elif choice == "3":
                self.reset_quiz_data()
            elif choice == "4":
                print("Thank you for using the Quiz System! Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    def handle_quiz_session(self):
        # handles the quiz session where users can take the quiz
        while True:
            print("\n" * 2)
            print("=== NEW QUIZ SESSION ===")
            
            # get the user's name
            name = self.get_user_name()
            user = QuizTaker(name)
            
            # run the quiz
            self.take_quiz(user)
            
            # show their results
            self.show_individual_results(user)
            self.quiz_takers.append(user)
            
            # ask if someone else wants to take it
            while True:
                another = input("\nDoes anybody else want to take the quiz? (y/n): ")
                another = another.strip().lower()
                if another == 'y' or another == 'yes' or another == 'n' or another == 'no':
                    break
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
            
            if another == 'n' or another == 'no':
                print("\n" * 2)
                print("=== FINAL RESULTS ===")
                self.show_overall_statistics()
                break

def main():
    # start the quiz system
    try:
        quiz_system = QuizSystem()
        quiz_system.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# run the program
if __name__ == "__main__":
    main()
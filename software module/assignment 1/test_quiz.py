"""
Test script for Quiz Application - Automated Testing
This script demonstrates the quiz functionality programmatically
"""

import sys
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from quiz_application import (
    get_quiz_questions,
    check_answer,
)

def test_question_bank():
    """Test that question bank loads correctly"""
    print("="*70)
    print("TEST 1: Question Bank Loading")
    print("="*70)
    
    questions = get_quiz_questions()
    print(f"[PASS] Total questions loaded: {len(questions)}")
    print(f"[INFO] Expected: 11 questions")
    
    assert len(questions) == 11, "Should have 11 questions"
    
    # Check question structure
    for idx, q in enumerate(questions, 1):
        assert 'question' in q, f"Question {idx} missing 'question' field"
        assert 'answer' in q, f"Question {idx} missing 'answer' field"
        assert 'explanation' in q, f"Question {idx} missing 'explanation' field"
    
    print("[PASS] All questions have required fields")
    print("[PASS] TEST 1 PASSED\n")


def test_answer_checking():
    """Test answer validation logic"""
    print("="*70)
    print("TEST 2: Answer Checking Logic")
    print("="*70)
    
    # Test single answer
    assert check_answer("dogs", "dogs") == True
    print("[PASS] Exact match works")
    
    # Test case insensitivity
    assert check_answer("dogs", "Dogs") == True
    assert check_answer("DOGS", "dogs") == True
    print("[PASS] Case insensitive matching works")
    
    # Test wrong answer
    assert check_answer("cats", "dogs") == False
    print("[PASS] Wrong answer detection works")
    
    # Test multiple acceptable answers
    assert check_answer("pinky", ["pinky", "inky", "blinky", "clyde"]) == True
    assert check_answer("blinky", ["pinky", "inky", "blinky", "clyde"]) == True
    assert check_answer("ghost", ["pinky", "inky", "blinky", "clyde"]) == False
    print("[PASS] Multiple acceptable answers work")
    
    # Test numeric answers
    assert check_answer("7", "7") == True
    assert check_answer("7", 7) == True
    print("[PASS] Numeric answer matching works")
    
    print("[PASS] TEST 2 PASSED\n")


def display_all_questions():
    """Display all quiz questions for review"""
    print("="*70)
    print("ALL QUIZ QUESTIONS AND ANSWERS")
    print("="*70)
    
    questions = get_quiz_questions()
    
    for idx, q in enumerate(questions, 1):
        print(f"\n{idx}. {q['question']}")
        
        answer = q['answer']
        if isinstance(answer, list):
            print(f"   Answer: {' or '.join(answer)}")
        else:
            print(f"   Answer: {answer}")
        
        print(f"   Note: {q['explanation']}")
    
    print("\n" + "="*70)


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print(" "*15 + "QUIZ APPLICATION - AUTOMATED TESTS")
    print("="*70 + "\n")
    
    try:
        test_question_bank()
        test_answer_checking()
        display_all_questions()
        
        print("\n" + "="*70)
        print("[SUCCESS] ALL TESTS PASSED SUCCESSFULLY!")
        print("="*70)
        print("\nThe quiz application is ready to use.")
        print("Run: python quiz_application.py")
        print("="*70 + "\n")
        
    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}")


if __name__ == "__main__":
    main()


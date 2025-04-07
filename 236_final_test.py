import csv
import random
import re
import time
import os
import sys

# --- Constants ---
TIME_LIMIT_SECONDS = 600  # 10 minutes

# --- Load questions from CSV ---
def load_questions_from_csv(filename="cpsc236_testbank.csv"):
    """Load questions from a CSV file into a list of dictionaries."""
    questions = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                questions.append({
                    "question": row["Question"],
                    "options": [
                        f"A) {row['A']}",
                        f"B) {row['B']}",
                        f"C) {row['C']}",
                        f"D) {row['D']}"
                    ],
                    "answer": row["Answer"].strip().upper()
                })
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        sys.exit()
    return questions

# --- ID Validation ---
def validate_id(student_id):
    """Validate that the ID starts with 'A' followed by 5 digits between 1 and 9."""
    return bool(re.match(r"^A[1-9]{5}$", student_id))

# --- Get Student Info ---
def get_student_info():
    """Prompt student for name and ID, with validation and 3 retry attempts."""
    first_name = input("Enter your first name: ").strip()
    last_name = input("Enter your last name: ").strip()

    attempts = 0
    while attempts < 3:
        student_id = input("Enter your Student ID (e.g., A12345): ").strip()
        if validate_id(student_id):
            return first_name, last_name, student_id
        else:
            print("Invalid ID format. Try again.")
            attempts += 1
    print("Too many failed attempts. Exiting.")
    sys.exit()

# --- Question Count Selection ---
def choose_question_count():
    """Allow student to choose 10 or 20 questions."""
    while True:
        choice = input("Do you want to take a 10 or 20 question quiz? (Enter 10 or 20): ").strip()
        if choice in ['10', '20']:
            return int(choice)
        else:
            print("Invalid input. Please enter 10 or 20.")

# --- Select Random Questions ---
def get_random_questions(question_pool, num_questions):
    """Select a number of unique random questions from the pool."""
    return random.sample(question_pool, num_questions)

# --- Ask Questions and Record Answers ---
def ask_questions(questions, start_time, time_limit):
    """Display questions one by one, record answers, and track time."""
    answers = []
    for i, q in enumerate(questions, 1):
        elapsed = time.time() - start_time
        if elapsed > time_limit:
            print("\n⏱️ Time is up! Submitting the quiz...\n")
            break

        print(f"\nQuestion {i}: {q['question']}")
        for option in q['options']:
            print(option)

        while True:
            answer = input("Enter your answer (A, B, C, or D): ").strip().upper()
            if answer in ['A', 'B', 'C', 'D']:
                break
            else:
                print("Invalid input. Please enter A, B, C, or D.")

        answers.append({"question": q['question'], "correct": q['answer'], "student_answer": answer})
    return answers

# --- Calculate Score ---
def calculate_score(answers, question_count):
    """Calculate score based on correct answers and quiz type."""
    correct_count = sum(1 for a in answers if a['correct'] == a['student_answer'])
    score = correct_count if question_count == 10 else correct_count * 0.5
    return score

# --- Save Results to File ---
def save_results(student_id, first_name, last_name, score, elapsed_time, answers):
    """Write quiz results to a personalized text file."""
    filename = f"{student_id}_{first_name}_{last_name}.txt"
    with open(filename, 'w') as f:
        f.write(f"Student ID: {student_id}\n")
        f.write(f"Name: {first_name} {last_name}\n")
        f.write(f"Score: {score:.2f} / 10\n")
        f.write(f"Elapsed Time: {elapsed_time:.2f} seconds\n\n")
        for i, entry in enumerate(answers, 1):
            f.write(f"Q{i}: {entry['question']}\n")
            f.write(f"Correct Answer: {entry['correct']}, Your Answer: {entry['student_answer']}\n\n")
    print(f"\n✅ Results saved to {filename}")

# --- Main Program Loop ---
def main():
    """Main program loop for handling quiz sessions."""
    question_pool = load_questions_from_csv()

    while True:
        first_name, last_name, student_id = get_student_info()
        question_count = choose_question_count()

        if question_count > len(question_pool):
            print("Not enough questions in the test bank.")
            break

        questions = get_random_questions(question_pool, question_count)

        print("\n📚 Starting the quiz! You have 10 minutes.\n")
        start_time = time.time()
        answers = ask_questions(questions, start_time, TIME_LIMIT_SECONDS)
        elapsed = time.time() - start_time

        score = calculate_score(answers, question_count)
        print(f"\n🎯 Your score: {score:.2f} / 10")
        print(f"⏱️ Time taken: {elapsed:.2f} seconds")

        save_results(student_id, first_name, last_name, score, elapsed, answers)

        choice = input("\nEnter Q to quit or S to start a new quiz: ").strip().upper()
        if choice == 'Q':
            print("Goodbye!")
            break
        elif choice == 'S':
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("Invalid input. Exiting.")
            break

# --- Run the Program ---
if __name__ == "__main__":
    main()
def create_quiz(quiz_data):
    print("Welcome to the Quiz! Answer the following questions:")

    score = 0
    total_questions = len(quiz_data)

    for question_data in quiz_data:
        question = question_data['question']
        options = question_data['options']
        correct_answer = question_data['correct_answer']

        print("\n" + question)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        user_answer = int(input("Enter the number of your answer: "))
        if options[user_answer-1] == correct_answer:
            print("Correct!")
            score += 1
        else:
            print("Incorrect.")

    print(f"\nYour score: {score}/{total_questions}")


if __name__ == '__main__':
    quiz_data = [
        {
            'question': 'What is the capital of France?',
            'options': ['Paris', 'Berlin', 'London'],
            'correct_answer': 'Paris'
        },
        {
            'question': 'Which one is a programming language?',
            'options': ['Python', 'HTML', 'CSS'],
            'correct_answer': 'Python'
        },
        {
            'question': 'What is the largest mammal on Earth?',
            'options': ['Elephant', 'Blue Whale', 'Giraffe'],
            'correct_answer': 'Blue Whale'
        }
    ]

    create_quiz(quiz_data)
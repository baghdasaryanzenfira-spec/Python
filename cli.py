#!/usr/bin/python3
question = "What is the capital of France?"
answer = "paris"
hidden_answer = "-" * len(answer)
print(question)
while "-" in hidden_answer:
    print(hidden_answer)
    letter = input("Enter a letter: ").lower()
    if letter in answer:
        new_hidden_answer = ""
        for i in range(len(answer)):
            if answer[i] == letter:
                new_hidden_answer += letter
            else:
                new_hidden_answer += hidden_answer[i]
        hidden_answer = new_hidden_answer
        print("Correct!")
    else:
        print("No such letter!")
print(f"Win! {answer}")

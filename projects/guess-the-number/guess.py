import random
print("Hello, What is your name?")
name = input()

print("Well", name, "I am thinkng of a number between 1 and 20.")
secretNumber = random.randint(1, 20)
print("DEBUG: The secret number is: ", str(secretNumber))  # This id just for debugging purpose

#Player a guess a max of 6 times
for guessTaken in range(1, 7):
    print("Take a guess")
    guess = int(input())  # converting string which was provided by input() into int type
    if guess > secretNumber:
        print("Too High")
    elif guess < secretNumber:
        print("Too low")
    else:  # This will execute only for correct guess with max limit of 6 guess
        print("Good Job, " + name + "! You guessed my number in " + str(guessTaken) + " guesses!")
        break  
else:  # This else belongs to "for" loop and this will execute when for loop iterations gets completed
    print("Nope!. The number I was thinking of was " + str(secretNumber))
    

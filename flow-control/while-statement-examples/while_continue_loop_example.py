spam = 0

while spam < 5:
    spam = spam + 1
    if spam == 3:
        continue  # when continue is executed, the execution will jump back to the start of while loop
    print("spam is: " + str(spam))
def plusOne():
    print("Please enter any number")
    number = input()
    return int(number) + 1  # when plusOne() function called, this line will just return the value won't print 
                     # on the terminal and that's why while calling the function, we assign the new variable and
                     # then call the function

newNumber = plusOne() # calling plusOne() function and storing the returned value into the new variable

print("The new number is:",newNumber)
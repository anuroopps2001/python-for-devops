# This program says hello and asks for myname and myage

print('Hello World.!')
print('What is your name?')  # ask for the user name
myName = input()  # input functions always returns strings

print("========")
print("It's good to meet you " + myName)
print('The length of your name is:') 
print(len(myName))

print('What is your age?')  # ask for the user age
myAge = input()   # input functions always returns strings

print(myName + ' you will be ' + str(int(myAge) + 1) + ' by next year' )
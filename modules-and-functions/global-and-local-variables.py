spam = 42 # global variable since it;s in global scope

def eggs():
    spam = 42  # local variable since its defined within an function which serves as a local scope

print("some code here.") # global scope
print("some more code.")  # global scope



# Assigning values to global variables from local scope of any function
def spam():
    global eggs  # global keyword is used to work of global variables from an local scope
    eggs = "hello"
    print(eggs)

eggs = 42
spam()
print(eggs)
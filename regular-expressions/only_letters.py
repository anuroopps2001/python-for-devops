import re

validator = re.compile(r"^[a-zA-Z]+$")  # This is an regular expression

user_input = input("Please enter your name: ")

match = validator.match(user_input)  # 

if match: # will be executed if the condition is True
    print("Clean Input")
else:
    print("Invalid Input, allowed only characters...!!")


import re

my_machine = re.compile(r"dev|staging") # Now, my_machine will be an object having lot of methods in it.

user_input = "dev"

result = my_machine.fullmatch(user_input)  # calling match of an my_machine object by passing arguement

print(result)
def eggs(cheese):
    # 'cheese' is a local variable that points to the SAME memory 
    # address as the 'spam' list created outside.
    cheese.append("Hello")
    # Because lists are "mutable" (changeable), modifying 'cheese' 
    # here affects the original data in memory.

# 1. 'spam' is created in memory. Let's say its address is 0x123.
spam = [1, 2, 3, 4, 5]

# 2. When we call eggs(spam), we aren't sending a copy of the list.
# We are sending the address 0x123 to the function.
eggs(spam)

# 3. Since the function modified the data at 0x123, 'spam' now reflects that.
print(spam)
# Output: [1, 2, 3, 4, 5, 'Hello']
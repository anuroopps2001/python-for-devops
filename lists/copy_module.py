import copy


spam = [1, 2, 3, 4, 5, 6]
print("Original spam list: ", spam)

cheese = copy.deepcopy(spam)

cheese[2] = "New_value"
print("Spam List after modified using copy module: ", cheese, \
      "and this is continued using line continuation concept in python and it;s \
       done using ''' \ ''' character..!!" \
      )

print("spam list: ", spam)
### List in python
- List is represented by [ ]
- Values inside the list are separated by comma (,)
- Values inside the list are called as items.


Creating an list :
```py
>>> ['cat', 'bat', 'elephant', 'zebra']
['cat', 'bat', 'elephant', 'zebra']
>>> spam = ['cat', 'bat', 'elephant', 'zebra']
>>> print(spam) 
['cat', 'bat', 'elephant', 'zebra']
>>> spam
['cat', 'bat', 'elephant', 'zebra']
>>>
```

- To access elements within a list, we use item's index Values :
```py
>>> spam
['cat', 'bat', 'elephant', 'zebra']
>>> spam[0]
'cat'
>>> spam[2]
'elephant'
>>> spam[5]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    spam[5]
    ~~~~^^^
IndexError: list index out of range
>>>
```

- List can contain, multiple lists inside of it.
```py
>>> spam = [['cat', 'bat', 'rat'], [10, 20, 30, 40, 50]]
>>> spam[0]
['cat', 'bat', 'rat']
>>> spam [0][2]
'rat'
>>> spam [1][3]
40
>>> spam [1]   
[10, 20, 30, 40, 50]
>>>
```

- We can use -ve indexes as well. and -1 will repesent last index and -2 will repesent last but 2nd index and so on :
```py
>>> spam = [['cat', 'bat', 'rat'], [10, 20, 30, 40, 50]]
>>> spam[-1]
[10, 20, 30, 40, 50]
>>> spam[-1][2]
30
>>> spam[-1][-2]
40
>>>
```

- String concatination using list items :
```py
>>> spam = [['cat', 'bat', 'rat'], [10, 20, 30, 40, 50]]
>>> print("The " + spam[0][-1] + " is afraid of " + spam[-2][0] + "!")
The rat is afraid of cat!
>>>
```

- `Slice` is used to get the range of values from an list and returns an new list
```py
>>> spam = [['cat', 'bat', 'rat'], [10, 20, 30, 40, 50]]
>>> spam[1][0:4]
[10, 20, 30, 40]
>>>
```

- Updating values of an list using their index :
```py
>>> spam = [1, 2, 3]
>>> spam
[1, 2, 3]
>>> spam[1] = "Hello"
>>> spam
[1, 'Hello', 3]
>>> spam[0] = True
>>> spam
[True, 'Hello', 3]
>>>
```

- Leaving out first or last index while accessing from an list using slice :
```py
>>> spam[1:3] = ["CAT", "RAT", "MOUSE"]
>>> spam
[True, 'CAT', 'RAT', 'MOUSE']
>>> spam[1:]  # from 1st index to end of an list
['CAT', 'RAT', 'MOUSE']
>>> spam[:3]  # 0 index is included and excluding 3rd index
[True, 'CAT', 'RAT']
>>>
```

- `del` keyword is used to delete an item from an list at specific index
```py
>>> spam
[True, 'CAT', 'RAT', 'MOUSE']
>>> del spam[0]  # delete item at 0 index
>>> spam
['CAT', 'RAT', 'MOUSE']
>>>
```

- `len` function is used to get the length of an list
```py
>>> spam
['CAT', 'RAT', 'MOUSE']
>>> len(spam)
3
>>> len(["1m", "2m", "3m"])
3
>>>
```

- list concatination :
```py
>>> [1, 2, 3] + [6, 5, 4]
[1, 2, 3, 6, 5, 4]
```

- `in` and `notin` operators can also be used with list :
```py
>>> 'howdy' in ['hello', 'hi', 'howdy', 'jimmy']
True
>>>

>>> 'smith' in ['hello', 'hi', 'howdy', 'jimmy']
False
>>>


>>> 'smith' not in ['hello', 'hi', 'howdy', 'jimmy']
True
>>>
```

- Replication of an list using `*` :
```py
>>> spam
[1, 2, 3]
>>> spam * 3
[1, 2, 3, 1, 2, 3, 1, 2, 3]
>>>
```

- `for` loop using an list :
```py 
for i in range(4):  # range is infact an list range(0,3)
    print(i)


AND

for i in [0, 1, 2, 3]:
    print(i)

BOTH DOES THE SAME JOB..!!
```

- `list` function can be used :
```py
>>> list(range(4))
[0, 1, 2, 3]
>>>

>>> list(range(0, 100, 2)) # 2 is an step value here
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98]
>>>
```

- Storing the values at specific index into new variable from an list i,e `Multiple Assignments`:
```py
>>> cat = ['fat', 'orange', 'angry']
>>> size, color, discription = cat
>>> size
'fat'
>>> color       
'orange'
>>> discription 
'angry'
>>>

OR

>>> size = cat[0]
>>> size
'fat'
>>> mood = cat[2]
>>> mood
'angry'
>>>
```

- Swapping of values :
```py
>>> a = "AAAA"
>>> b = "BBBB"
>>> a, b = b, a
>>> a
'BBBB'
>>> b
'AAAA'
>>>
```

- `Augmented operators` : +, -, *, / and % 
```py
>>> spam = 42
>>> spam = spam + 2  # Augmented operator
>>> spam += 1  # Augmented operator
>>> spam
45
>>>
```

### List Methods :- These are similar to functions and they work on the lists.
- `index` method
```py
>>> spam = ['hello', 'ola', 'hi']  
>>> print(spam)
['hello', 'ola', 'hi']
>>> spam.index('hello')  # index is an method here and working on spam list
0
>>>

# If we have duplicate values in an list, index method will return the index value of first occurance of the value
>>> spam = ['cat', 'bat', 'rat', 'cat']
>>> spam.index('cat')
0
>>>
```

- `append` method: This will add the value at the end of an list :
```py
>>> spam.append('Monkey')
>>> spam
['cat', 'bat', 'rat', 'cat', 'Monkey']
>>>
```

- `insert` method: This works exactly like `append` method but it will insert the values at required index of an list :
```py
>>> ['cat', 'bat', 'rat', 'cat', 'Monkey']
>>> spam.insert(2, 'dog')     
>>> spam
['cat', 'bat', 'dog', 'rat', 'cat', 'Monkey']
>>>
```

- `remove` method : Used to remove an specific element from an list
```py
>>> spam = ['cat', 'bat', 'rat', 'elephant']
>>> spam
['cat', 'bat', 'rat', 'elephant']
>>> spam.remove('elephant')
>>> spam
['cat', 'bat', 'rat']
>>>

# If there are duplicate values and want to remove, remove method will remove only the first occurance of that value
>>> spam = ['cat', 'hat', 'bat', 'cat', 'rat', 'cat', 'cat']
>>> spam
['cat', 'hat', 'bat', 'cat', 'rat', 'cat', 'cat']
>>> spam.remove('cat')
>>> spam
['hat', 'bat', 'cat', 'rat', 'cat', 'cat']
>>>
```

- `sort` method : Used to sort the values inside an list
```py
>>> spam = ['cat', 'hat', 'bat', 'cat', 'rat', 'cat', 'cat']
>>> spam.sort()
>>> spam
['bat', 'cat', 'cat', 'cat', 'cat', 'hat', 'rat']

# We can also use reverse keyword to reverse the sorting
>>> spam.sort(reverse=True)
>>> spam
['rat', 'hat', 'cat', 'cat', 'cat', 'cat', 'bat']
>>>

>>> spam = [9, 3.23, -2, 38, -23]
>>> spam.sort()
>>> spam
[-23, -2, 3.23, 9, 38]
>>>
>>>

# Python cannot sort if list contains values of different data types
>>> spam = [1, 2, 3, 'Alice', 'Bob']
>>> spam
[1, 2, 3, 'Alice', 'Bob']
>>> spam.sort()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    spam.sort()
    ~~~~~~~~~^^
TypeError: '<' not supported between instances of 'str' and 'int'
>>>


#ASCII-betical order of sorting
>>> spam = ['a', 'x', 'A', 'X', 'n']
>>> spam.sort()
>>> spam
['A', 'X', 'a', 'n', 'x']
>>>

>>> spam.sort(key=str.lower)  
>>> spam
['A', 'a', 'n', 'X', 'x']
>>>
```

**List and strings a most of the similarities. However, strings are immutable and lists are mutable in nature**


#### *`IMPORTANT`*
**Also, when we assign the one variable containing a list into another variable, modifying the second will variable will affect the original list**

```py
>>> spam = [1,2,3,4,5,6]
>>> spam
[1, 2, 3, 4, 5, 6]
>>>
>>> 
>>> cheese = spam
>>> cheese
[1, 2, 3, 4, 5, 6]
>>> cheese[1] = "Bye"
>>> cheese
[1, 'Bye', 3, 4, 5, 6]
>>> spam
[1, 'Bye', 3, 4, 5, 6]
>>>
```

**So, to work on original list, instead of it;s reference, we can use `copy` module**

- Line continuation for lists : It;s done by addding \ at the end of the print function
```py
>>> spam = ['Hello',
...         'Hi',
...         'Ola',
...         'Bye']
>>> spam
['Hello', 'Hi', 'Ola', 'Bye']
>>>
```


### tuple is same as list, except tuples are immutable and represented using ()

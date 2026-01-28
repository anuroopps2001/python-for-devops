# Python

string concatination

```bash
>>> 'alice' + ' ' + 'bob'
'alice bob'
```

string replication

```bash
>>> 'hello' + '!' * 10
'hello!!!!!!!!!!'
```

variables

```bash
>>> spam = 43
>>> print(spam)
43
>>> spam
43
>>> spam = 'Hello'  # overriding the value of a variable
>>> spam + 'world'
'Helloworld'
>>> spam + ' world'
'Hello world'
>>>
>>> spam = 10 + 10
>>> spam
20
>>> spam = spam + 11
>>> spam
31
>>>
```

data types conversions

```bash
>>> str(25)
'25'
>>> int('28')
28
>>> float(15)
15.0
>>> int(17.93)
17
>>> float('3.145')
3.145
```

Boolean values

```bash
True
False
```

Comparison operators:
Expressions of comparison operators will return Boolean values as result

```bash
==
!=
<
>
<=
>=

>>> 23 == 244
False
>>> 247 != 2
True
>>> 2 > 38
False
>>> 34 < 32
False
>>> 23 == '23'
False
>>> myAge = 25
>>> myAge < 23
False
>>>
>>> 42 == 42.00
True
```

Boolean operators

```bash
and
or
not

>>> True and True
True
>>> True and False
False
>>> False and False
False
>>> False and True
False
>>>

>>> True or True
True
>>> False or True
True
>>>

>>> not True
False
>>> not False
True
>>>

>>> myAge = 26
>>> myPet = 'cat'
>>> myAge > 20 and myPet == 'cat'
True
>>>

>>> myAge
26
>>> not (myAge <= 26)
False
```

`break` and `continue` statements can be used within `for` loops as well and work exactly the same way as they work for `while` loops.

*`range` is a built-in function which includes the start value and excludes the last value. It can also be called by providing a third argument called the `step` value.*

---

## Modules in Python

A module is a collection of custom functions.

### Importing Modules

```bash
>>> import random
>>> random.randint(19, 27)
24
>>> random.randint(19, 27)
27
>>> random.randint(19, 27)
22
>>>
```

Other way:

```bash
>>> from random import *
>>> randint(12, 143)
137
>>> randint(12, 143)
33
>>> randint(12, 143)
130
>>> randint(12, 143)
130
>>>
```

Importing multiple modules at once

```bash
>>> import random, math, sys, os
```

---

### Using third-party Modules

#### Download `pyperclip` module using `pip` package manager

```bash
C:\Users\ANUROOP P S>C:\Python314\Scripts
'C:\Python314\Scripts' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\ANUROOP P S>cd C:\Python314\Scripts

C:\Python314\Scripts>
C:\Python314\Scripts>pip install pyperclip
Defaulting to user installation because normal site-packages is not writeable
Collecting pyperclip
  Downloading pyperclip-1.11.0-py3-none-any.whl.metadata (2.4 kB)
Downloading pyperclip-1.11.0-py3-none-any.whl (11 kB)
Installing collected packages: pyperclip
Successfully installed pyperclip-1.11.0

[notice] A new release of pip is available: 25.2 -> 25.3
[notice] To update, run: python.exe -m pip install --upgrade pip

C:\Python314\Scripts>python.exe -m pip install --upgrade pip
Defaulting to user installation because normal site-packages is not writeable
Requirement already satisfied: pip in c:\python314\lib\site-packages (25.2)
Collecting pip
  Downloading pip-25.3-py3-none-any.whl.metadata (4.7 kB)
Downloading pip-25.3-py3-none-any.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 1.2 MB/s  0:00:01
Installing collected packages: pip
Successfully installed pip-25.3

C:\Python314\Scripts>
```

**`pip` is the package manager used to download, install, upgrade, and remove third-party Python modules (libraries).**

---

#### Using `pyperclip` module and its functions

```bash
>>> import pyperclip
>>> pyperclip.copy("This text will be copied into clipboard")
>>> pyperclip.paste()
'This text will be copied into clipboard'
>>>
```

*`pyperclip.copy(text)` function is used to copy the data to the clipboard and `pyperclip.paste()` is used to retrieve that data.*

---

## Functions in Python

### Example 01

```bash
def hello(name):  # Parameter
    print("hello", name)

# calling hello() function
hello('Alice')  # Argument
hello('Bob')
```

### Example 02

```bash
def hello():  # def is the keyword used to define functions in Python (similar to func in Golang)
    print("Howdy.!" )
    print("Howdy.!!!")
    print("Hello there.")

print("Calling hello() function for the first time")
hello()

print("Calling hello() function for the second time")
hello()

print("Calling hello() function for the third time")
hello()
```

* **Parameter**: The variable inside the function definition.
* **Argument**: The value passed during the function call.

**Every function has a return value. If not explicitly returned, the default return value is `None`. Even the `print()` function returns `None`.**

```bash
>>> spam = print()
>>> spam == None
True
>>>
```

*When `print()` is called with no arguments, it returns a `None` value.*

---

### Keyword arguments

*By default, the `print()` function appends a newline character (`\n`) at the end.*

`keyword_args.py`

```py
print("hello")  # newline causes next output on new line
print("bob")
```

Output:

```bash
$ py keyword_args.py
hello
bob
```

`second_example.py`

```py
print("This won't create a new line", end=' ')  # adding space at the end
print("This line will be appended")
```

Output:

```bash
$ py second_example.py
This won't create a new line This line will be appended
```

**Default separator in `print()` is a blank space and we can customize it using the `sep` keyword.**

```py
>>> print('cat', 'dog', 'mouse')
cat dog mouse
>>> print('cat', 'dog', 'mouse', sep="ABCD")
catABCDdogABCDmouse
>>>
```

---

### Global and Local Variables

**Variables assigned outside all functions are global variables. Variables defined inside a function are local variables for that function.**

`global-and-local-variables.py`

```py
spam = 42  # global variable

def eggs():
    spam = 42  # local variable

print("some code here.")
print("some more code.")
```

* **Local scope code can use global scope variables.**

```py
def spam():
    print(eggs)  # using global variable inside local scope

eggs = 42
spam()
```

Output:

```bash
42
```

* **Global scope code cannot use local scope variables.**

```py
def spam():
    eggs = 92

spam()
print(eggs)  # This will throw an error
```

Output:

```bash
NameError: name 'eggs' is not defined
```

* **One function's local scope variables cannot be used in another function's local scope.**

```py
def spam():
    eggs = 92
    bacon()
    print(eggs)

def bacon():
    ham = 101
    eggs = 0

spam()
```

---

### Assigning values to global variables from local scope

```py
def spam():
    global eggs
    eggs = "hello"
    print(eggs)

eggs = 42
spam()
print(eggs)
```

Output:

```bash
hello
hello
```

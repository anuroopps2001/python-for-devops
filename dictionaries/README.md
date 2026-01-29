## Dictionary :
#### Dictionary is an collection of key-value pairs
```py
>>> myCat = {'size': 'fat', 'color': 'grey', 'dispositon': 'loud'}
>>> type(myCat)
<class 'dict'>
>>> myCat['size']
'fat'
>>> print("My Cat has a " + myCat['color'] + " colour") 
My Cat has a grey colour
>>>
```

- Dictionaries are unordered in nature.
```py
>>> [1, 2, 3] == [2, 3, 1]
False
>>> eggs = {'name': 'Zophie', 'species': 'cat', 'age': 9}
>>> ham = {'age': 9, 'name': 'Zophie', 'species': 'cat'}
>>> eggs == ham  # order is different, but still retuns True
True
>>>
```
- Trying to access the key, that doesn;t exists in the Dictionary, will result in KeyError
```py
>>> eggs['color']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    eggs['color']
    ~~~~^^^^^^^^^
KeyError: 'color'
>>>
```

- We can use `in` and `not in` operators along with the keys to check whether that specific key exists or not inside the Dictionary
```py
>>> eggs = {'name': 'Zophie', 'species': 'cat', 'age': 9}
>>> 'name' in eggs
True
>>> 'name' not in eggs
False
>>>

{'name': 'Zophie', 'species': 'cat', 'age': 9}
>>> 'color' in eggs.keys()
False
>>> 'color' not in eggs.keys()
True
>>> 'shape' in eggs.values()  
False
>>> 'structure' in eggs.item()  
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
    'structure' in eggs.item()
                   ^^^^^^^^^
AttributeError: 'dict' object has no attribute 'item'. Did you mean: 'items'?
>>> 'structure' in eggs.items()
False
>>>
```

**Dictionary are mutuable in nature like Lists does.**

- Creating an list based on keys, values or both keys and values of an Dictionary
```py
>>> eggs = {'name': 'Zophie', 'species': 'cat', 'age': 9}
>>> list(eggs.keys())
['name', 'species', 'age']
>>> list(eggs.values())
['Zophie', 'cat', 9]
>>> list(eggs.items())
[('name', 'Zophie'), ('species', 'cat'), ('age', 9)]
>>>
```

- Usage in for loop :
```py
>>> for k in eggs.keys:
...    print(k)

name
specific
age

>>> for v in eggs.values:
...    print(v)
Zophie
cat
9
```


- `get` method can be used with Dictionaries, to see the whether the key actually exists or not and if it doesn;t exists, retun a fallBack value and `get` method takes 2 args, i,e key_name and the fallBack_value

```py
>>> eggs
{'name': 'Zophie', 'species': 'cat', 'age': 9}
>>> eggs.get('age', 0)  # 0 is the fallBack value here
9
>>> eggs.get('size', 'fat')  # 'fat' is the fallBack value
'fat'
>>>
>>> eggs.get('color', '')
''
>>>


>>> picnicItems = {'apples': 5, 'cups': 2}
>>> picnicItems
{'apples': 5, 'cups': 2}
>>> print("I am bringing " + str(picnicItems.get('napkins', 0)) + " napkins to the picnic")
I am bringing 0 napkins to the picnic
>>
```

- `setdefault` is an method which is used to set an key an only if it doesn;t exists by default
```py
>>> eggs
{'name': 'Zophie', 'species': 'cat', 'age': 9}
# since 'color' key doesn;t exists by default, python will add it
>>> eggs.setdefault('color', 'black')
'black'
>>> eggs
{'name': 'Zophie', 'species': 'cat', 'age': 9, 'color': 'black'}
>>>

>>> eggs.setdefault('color', 'orange')
'black'
>>> eggs  # because, 'color' key already exists
{'name': 'Zophie', 'species': 'cat', 'age': 9, 'color': 'black'}
>>>
```


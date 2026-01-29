ham = {'age': 9, 'name': 'Zophie', 'species': 'cat'}

print("All the keys of an Dictionary are: ")
for k in ham.keys():   # keys() is a method which returns only the keys froom an Dictionary
    print(k)

print("==============")

print("All the values of an Dictionary are: ")

for v in ham.values():  # values() is an method which returns only the values from an Dictionary
    print(v)


print("==============")

print("All the key-value pairs of an Dictionary are: ")
for k, v in ham.items():  # items() is an method which returns both keys and values from an Dictionary
    print(k,v)

print("Set of key-value pairs of an Dictionary")
for i in ham.items():
    print(i)



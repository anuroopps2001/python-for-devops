def parse_int(value):
    try:
        num = int(value)

        if num <= 0:
            return None, ValueError("Number must be greater than 0")
        else:
            return num, None
        
    except Exception as e:  # If i don;t the exact error
        return None, e
    
print("How many cats do you have?")
nunCats = input()  # input function always stores data in the form of strings

cats, err = parse_int(nunCats)

if err:
    print(type(err))  # get the type of the eror and then update the parse_int function as except ValueError as e:
else: 
    if cats >= 4:
        print("That's a lot of cats")
    else:
        print("That;s not that many cats")


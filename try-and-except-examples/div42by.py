# def div42By(dividBy):
#     try:
#         return 42/dividBy
#     except ZeroDivisionError:
#         print("Error: You tried to divide by zero")

# print(div42By(2))
# print(div42By(21))
# print(div42By(0))
# print(div42By(1))


def div42By(x):
    if x == 0:
        return None, ValueError("divisible by zero")
    return 42/x, None



def safe_call(x):
    value, err = div42By(x)

    if err:
        print("error:", err)
    else:
        print(value)

safe_call(2)
safe_call(21)
safe_call(0)
safe_call(42)
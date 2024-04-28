from random import randint

# Test function
def print_random_number(digits: int):
    if digits > 0:
        print(randint(0, 10**digits))
    else:
        print("Digits must be bigger then 0")

print_random_number(3)


#!/usr/bin/python


# BLACK HEART SUIT, hex 2665
x = "♥"
y = "\u2665"

print(x == y)
# True
print(x)
print(y)

# unicode escape sequence, for char with more than 4 hexadecimal digits

# GRINNING CAT FACE WITH SMILING EYES, hex 1f638
x = "😸"
y = "\U0001f638"

print(x == y)
# True
print(x)
print(y)

def ƒ(α):
    return α+1

n=10
print(f"😸{ƒ(n+5)}♥")

print("però")

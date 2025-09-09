a = int(input("Input 1: "))
b = int(input("Input 2: "))
c = int(input("Input 3: "))

if a >= b:
    if a >= c:
        print("Largest number is:", a)
    else:
        print("Largest number is:", c)
else:
    if b >= c:
        print("Largest number is:", b)
    else:
        print("Largest number is:", c)
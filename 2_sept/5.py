n = int(input("Input: "))
f = 1
i = 1
while i <= n:
    f *= i
    i += 1
    print(f)
print("Factorial :", f)
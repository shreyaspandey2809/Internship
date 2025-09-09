n = int(input("Input: "))
c = 0
while n > 0:
    n //= 10
    c += 1
print("Number of Digits:", c)
a= int(input("Input: "))
if a > 1:
    for i in range(2, a):
        if a % i == 0:
            print("not prime")
            break
    else:
        print("prime")
else:
    print("not prime")
a = "Honesty is the best policy"
b = a.split()
c = len(b)
d = []
for i in range (c-1 , -1 , -1):
    d.append(b[i])
e = " ".join(d)
print(e)
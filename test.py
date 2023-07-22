x = 6
for i in range(x):
    if i % 2 == 0:
        flag = False
    else:
        flag = True
    for n in range(x):
        if flag:
            if (n % 2 != 0):    
                print("*", end="")
            else:
                print("_",end="")
        else:
            if (n % 2 != 0):
                print("_", end="")
            else:
                print("*",end="")
    print("")
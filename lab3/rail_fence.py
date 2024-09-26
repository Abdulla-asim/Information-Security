import math as m

def rail_fence(text, key):
    #rows = int(input("Enter the key (int): "))
    rows = key
    #text = input("Enter the message: ")
    length = len(text)

    matrix = [[] for _ in range (rows)]

    x = 0
    direction = 1;
    i = 0

    while True:
        if (i >= length):
            matrix[x].append('x')
        else:
            matrix[x].append(text[i])
            
        if (x >= rows-1):
            if (length <= i):
                break
            direction = -1 
        elif (x == 0):
            direction = 1
        x += direction
        i += 1

    cipher_text = ""
    for row in matrix:
        for col in row:
            cipher_text += col

    return cipher_text


print (rail_fence("Information", 4))
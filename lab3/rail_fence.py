def rail_fence_encrypt(text, key):

    #rows = int(input("Enter the key (int): "))
    rows = key
    #text = input("Enter the message: ")
    length = len(text)

    matrix = [[] for _ in range (rows)]

    index = 0
    direction = 1;
    i = 0 # Text letters index

    while True:
        if (i >= length):
            matrix[index].append('x')
        else:
            matrix[index].append(text[i])
            
        if (index == rows-1):
            if (i >= length):
                break
            direction = -1 
        elif (index == 0):
            direction = 1
        index += direction
        i += 1

    for r in matrix:
        print(r)

    cipher_text = ""
    for row in matrix:
        for col in row:
            cipher_text += col

    return cipher_text

def rail_fence_decrypt(cipher_text, key):
    rows = key
    matrix = [[] for _ in range(rows)]
    length = len(cipher_text)

    


print(f"Cipher Text: {rail_fence_encrypt("Information", 4)}")
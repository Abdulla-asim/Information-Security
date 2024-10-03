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

    # For printing the matrix that was created
    #for r in matrix:
    #   print(r)

    cipher_text = ""
    for row in matrix:
        for col in row:
            cipher_text += col

    return cipher_text

def rail_fence_decrypt(cipher_text, key):
    rows = key
    length = len(cipher_text)
    matrix = [['\n' for _ in range(length)] for _ in range(rows)]

    index = 0
    direction = 1
    for i in range(length):
        matrix[index][i] = '*'
        if (index == rows-1):
            direction = -1
        elif (index == 0):
            direction = 1
        index += direction

    index = 0
    for i in range(rows):
        for j in range(length):
            if (matrix[i][j] == '*'):
                matrix[i][j] = cipher_text[index]
                index += 1

    result = ""
    index = 0
    direction = 1
    for i in range(length):
        result += matrix[index][i]
        if (index == rows-1):
            direction = -1
        elif(index == 0):
            direction = 1
        index += direction

    return result

# Testing encryption and decryption
if __name__ == "__main__":
    key = int(input("Enter the key (int): "))
    cipher_text = rail_fence_encrypt("Information", key)
    print(f"Cipher Text: {cipher_text}")
    print(f"Decrypted Text: {rail_fence_decrypt(cipher_text, key)}")
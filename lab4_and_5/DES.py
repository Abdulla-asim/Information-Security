
def text_to_bits(text, encoding='utf-8'): 
    bits = ''
    for char in text:
        encoded_text = char.encode(encoding) # encode the character to utf-8 or anotehr encoding (e.g. ASCII)
        integer = int.from_bytes(encoded_text, 'big') # convert the encoded text to an integer (big endian format)
        bits += bin(integer)[2:].zfill(8) # convert the character to binary and add it to the bits
    return bits

def des_plaintext_block(text, block_size=64):
    blocks = [] # list to store the blocks
    bits = text_to_bits(text) # convert the text to bits
    bits = bits + "0" * (block_size - len(bits) % block_size) # pad the bits with zeros to make the length a multiple of block_size
    for i in range(0, len(bits), block_size):  # iterate over the bits in steps of block_size
        block = bits[i:i + block_size] # get one block of bits
        blocks.append(block) # add the block to the list of blocks

    return blocks

def des_initial_permutation(block : str):
    # initial permutation table
    IP_table = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

    # apply the initial permutation to the block
    permuted_block = ""
    for i in IP_table:
        permuted_block += block[i - 1]

    return permuted_block

def des_final_permutation(block : str):
    # final permutation table
    FP_table = [
        40, 8, 48, 16, 56, 24, 64, 32, 
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25
    ]

    # apply the final permutation to the block
    permuted_block = ""
    for i in FP_table:
        permuted_block += block[i - 1]
    
    return permuted_block


### LAB5 STARTS HERE
# Epxpansion pemutation for one plain text block
def expansion_permutation(block: str):
    E_table = [ # 8 x 6
        32,  1,  2,  3,  4,  5,
        4,   5,  6,  7,  8,  9, 
        8,   9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32,  1
    ]

    expanded_block = "" # 48 bit block in the end
    for i in E_table:
        expanded_block += block[i-1] # i-1 because index starts at 0
    
    return expanded_block


### KEY SCHEDULING FUNCTIONS
# Parity Drop for the key
def permuted_choice_1(key_64: str):
    parity_drop_table = [ 
        57 ,49, 41, 33, 25, 17, 9,
        1,  58, 50, 42, 34, 26, 18,
        10,  2, 59, 51, 43, 35, 27,
        19, 11,  3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
         7, 62, 54, 46, 38, 30, 22,
        14,  6, 61, 53, 45, 37, 29,
        21, 13,  5, 28, 20, 12,  4
    ]

    key_56 = ""
    for i in parity_drop_table:
        key_56 += key_64[i-1]

    return key_56

# Key left shift function
def left_shift(key_28: str, round_no: int):
    if round_no in [1, 2, 9, 16]:
        return key_28[1:] + key_28[0]
    else:
        return key_28[2:] + key_28[:2]

# for 56 to 48 bit key
def permuted_choice_2(key_56: str):
    PC2_table = [
        14, 17, 11, 24,  1,  5,
         3, 28, 15,  6, 21, 10,
        23, 19, 12,  4, 26,  8,
        16,  7, 27, 20, 13,  2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]

    key_48 = ""
    for i in PC2_table:
        key_48 += key_56[i-1]

    return key_48

# S-Boxes
def sub_boxes(expanded_block: str):
    # S-Box tables
    S_box = [
        # S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        # S2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        # S3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        # S4    
        [  
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        # S5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        # S6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        # S7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        # S8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]

    # Split the expanded block into 8 6-bit blocks
    blocks = [expanded_block[i: i+6] for i in range (0, len(expanded_block), 6)]

    # Apply the S-Boxes
    output = ""
    for i, block in enumerate(blocks):
        row = int(block[0] + block[5], 2)
        col = int(block[1:5], 2)
        value = S_box[i][row][col]
        output += format(value, '04b')

    return output


if __name__ == "__main__":
    plaintext = "hello"
    blocks = des_plaintext_block(plaintext) # get the blocks of the plaintext

    # print 8x8 matrix of the bits
    for i, block in enumerate(blocks):
        print(f"Block {i + 1}: ", end="")
        for j in range(0, len(block), 8):
            print(block[j: j + 8], end=" ")
        print()
    print()

    permuted_blocks = [] # list to store the permuted blocks
    # apply the initial permutation to the blocks
    for i, block in enumerate(blocks):
        permuted_block = des_initial_permutation(block)
        permuted_blocks.append(permuted_block)
        print(f"Initial Permutation Block {i + 1}: ", end="")
        for j in range(0, len(permuted_block), 8):
            print(permuted_block[j: j + 8], end=" ")
        print()
    print()
    
    # apply the final permutation to the permuted blocks
    for i, block in enumerate(permuted_blocks):
        final_permuted_block = des_final_permutation(block)
        print(f"Final Permutation Block {i + 1}: ", end="")
        for j in range(0, len(final_permuted_block), 8):
            print(final_permuted_block[j: j + 8], end=" ")
        print()
    print()

    expanded_blocks = [[] for _ in range(len(permuted_blocks))] # list to store the expanded blocks
    for i, block in enumerate(permuted_blocks):
        print(f"Expanded Block {i + 1}: ")
        for j in range(2):
            # Takes 32 bit block and expands it to 48 bits
            expanded_block = expansion_permutation(block[j*32 : 32 * (j+1)])
            expanded_blocks[i].append(expanded_block) # [[block1_left, block1_right], [block2_left, block2_right]] (example)

            block_position = "Left" if j == 0 else "Right"
            print(f"{block_position}: ", end="")
            for k in range(0, len(expanded_block), 6):
                print(expanded_block[k: k + 6], end=" ")
            print()
        print()

    # S-Boxes   
    for i, block in enumerate(expanded_blocks):
        print(f"S-Boxes Block {i + 1}: ")
        for j in range(2):
            s_box_output = sub_boxes(block[j])

            block_position = "Left" if j == 0 else "Right"
            print(f"{block_position}: ", end="")
            for k in range(0, len(s_box_output), 4):
                print(s_box_output[k: k + 4], end=" ")
            print()
        print()
    
    print("----Key Scheduling----")
    key_64 = "0001001100110100010101110111100110011011101111001101111111110001"
    print("Key 64: ", end="")
    for i in range(0, len(key_64), 8):
        print(key_64[i: i + 8], end=" ")
    print('\n')

    key_56 = permuted_choice_1(key_64)
    print("Key 56: ", end="")
    for i in range(0, len(key_56), 7):
        print(key_56[i: i + 7], end=" ")
    print('\n')

    key_56_left = key_56[:28]
    key_56_right = key_56[28:]

    for i in range(1, 17):
        key_56_left = left_shift(key_56_left, i)
        key_56_right = left_shift(key_56_right, i)

        key_56 = key_56_left + key_56_right
        print(f"Key 56 round {i}: ", end="")
        for j in range(0, len(key_56), 7):
            print(key_56[j: j + 7], end=" ")
        print()

        key_48 = permuted_choice_2(key_56)
        print(f"Key 48 Round {i}: ", end="")
        for j in range(0, len(key_48), 6):
            print(key_48[j: j + 6], end=" ")
        print("\n")
    
    
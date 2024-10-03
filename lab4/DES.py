
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



if __name__ == "__main__":
    plaintext = "hello world"
    blocks = des_plaintext_block(plaintext) # get the blocks of the plaintext

    # print 8x8 matrix of the bits
    for i, block in enumerate(blocks):
        print(f"Block {i + 1}: ", end="")
        for j in range(0, len(block), 8):
            print(block[j:j + 8], end=" ")
        print()
    print()

    permuted_blocks = [] # list to store the permuted blocks
    # apply the initial permutation to the blocks
    for i, block in enumerate(blocks):
        permuted_block = des_initial_permutation(block)
        permuted_blocks.append(permuted_block)
        print(f"Initial Permutation Block {i + 1}: ", end="")
        for j in range(0, len(permuted_block), 8):
            print(permuted_block[j:j + 8], end=" ")
        print()
    print()
    
    # apply the final permutation to the permuted blocks
    for i, block in enumerate(permuted_blocks):
        final_permuted_block = des_final_permutation(block)
        print(f"Final Permutation Block {i + 1}: ", end="")
        for j in range(0, len(final_permuted_block), 8):
            print(final_permuted_block[j:j + 8], end=" ")
        print()
    print()

    
    
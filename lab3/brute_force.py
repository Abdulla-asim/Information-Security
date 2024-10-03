from rail_fence import rail_fence_decrypt

def brute_force(text):
    print("\nText: ", text)
    for i in range(2, len(text)):
        print(f"key: {i}:", end=" ")
        print(rail_fence_decrypt(text, i))
        print()

if __name__ == "__main__":
    text_1 = "HOLELWRDLO"
    text_2 = "TAKTANTKDAAW"
    text_3 = "CTCROPHYARG"
    brute_force(text_1)
    brute_force(text_2)
    brute_force(text_3)
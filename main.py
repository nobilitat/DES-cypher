import sys
from MainWindow import *
from textwrap import wrap


INITIAL_PERMUTATION = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

FINAL_PERMUTATION = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17,	11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

PF = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]

FUNCTION_EXTENSION = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

NODE_TABLE = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

SHIFT_BIT = [
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
]


def convert_bin_to_hex(string):
    """Convert encrypted/decrypted binary to hex"""

    result = wrap(string, 8)
    result = "".join([hex(int(i, 2))[2:].zfill(2) for i in result])
    return result


def convert_bin_to_text(string):
    """Convert encrypted/decrypted binary to text"""

    result = wrap(string, 8)
    result = filter(lambda x: x != '00000000', result)
    result = "".join([chr(int(i, 2)) for i in result])
    return result


def prepare_key(key):
    """Prepare key list"""

    out = []
    key = convert_text_to_64(key)[0]
    key = convert_to_56(key)
    K1, K2 = wrap(key, 28)

    for i in range(16):
        key, K1, K2 = convert_key(i, K1, K2)
        out.append(key)

    return out


def convert_key(i, K1, K2):
    """Generate key for current iteration"""

    # Shift every part to left
    K1 = bin(int(K1, 2) << SHIFT_BIT[i] & 0x0fffffff | int(K1, 2) >> 28 - SHIFT_BIT[i])[2:].zfill(28)
    K2 = bin(int(K2, 2) << SHIFT_BIT[i] & 0x0fffffff | int(K2, 2) >> 28 - SHIFT_BIT[i])[2:].zfill(28)

    # Merge both parts
    key = K1 + K2

    # Last permutation key, 56-bit to 48-bit
    key = ''.join((key[i-1] for i in PC2))

    return [key, K1, K2]


def convert_to_56(text):
    """Convert 64-bit blocks to 56-bit"""

    return ''.join((text[i-1] for i in PC1))


def ip_execute(text):
    """Initial permutation"""

    return [''.join((j[i-1] for i in INITIAL_PERMUTATION)) for j in text]


def fp_execute(text):
    """Final permutation"""

    return ''.join([text[i-1] for i in FINAL_PERMUTATION])


def convert_text_to_64(text):
    """Convert source text to 64-bit"""

    # 1. convert to hexadecimal number
    result = [hex(ord(i))[2:] for i in text]

    # 2. split result text to 16 length string, out type - list
    result = wrap(''.join(result), 16)

    # 3. fill every element of hex number to 16 signs (1 element in hex == 2 bit)
    result = [i.zfill(16) for i in result]

    # 4. convert to binary number system
    result = convert_hex_to_bin(result)

    return result


def convert_hex_to_bin(text):
    """Convert number hex to binary number system"""

    return [bin(int(i, 16))[2:].zfill(64) for i in text]


def f(text, key):
    """
    Execution function F

    :param text: Text 32-bit
    :param key: Key 48-bit
    :return: Converted text 32-bit in binary system
    """

    # Convert text to 48-bit
    converted_text_to_48 = ''.join([text[i-1] for i in FUNCTION_EXTENSION])

    # XOR text 48-bit and key 48-bit
    result = bin(int(converted_text_to_48, 2) ^ int(key, 2))[2:].zfill(48)

    # Permutation with node table
    result = wrap(result, 6)
    result = [bin(NODE_TABLE[j][int(i[0]+i[-1], 2)][int(i[1:-1], 2)])[2:].zfill(4) for j, i in enumerate(result)]

    # Merge all parts
    result = ''.join(result)

    # Final permutation
    result = ''.join([result[i-1] for i in PF])

    return result


def ecb_algorithm(blocks, key_list):
    """
    Main algorithm for des

    :param blocks: blocks of original text
    :param key_list: list of keys for every round
    :return: results in hex number system and text
    """

    result = []

    # Initial permutation
    T_1 = ip_execute(blocks)
    print('\nT*: ', T_1)

    for i in T_1:
        print('\nBLOCK:', i)
        H, L = wrap(i, 32)

        for j, k in zip(range(1, 17), key_list):
            print('\nRound: ', j)
            print(f'\nH: {H} \nL: {L}')
            print('Generated key:', k)

            result_f = f(L, k)

            # XOR H and result function f
            H = bin(int(H, 2) ^ int(result_f, 2))[2:].zfill(32)

            # swap values
            H, L = [L, H] if j < 16 else [H, L]

        # Final permutation
        C = fp_execute(H + L)
        result.append(C)

    result_16 = ''.join([convert_bin_to_hex(i) for i in result])
    result_text = ''.join([convert_bin_to_text(i) for i in result])
    return result_16, result_text


def decrypt_ecb(text, key):
    """Decryption from hex to original text"""

    # Convert encrypted hex to 64-bit blocks
    text = wrap(text, 16)
    C = convert_hex_to_bin(text)

    key_list = prepare_key(key)
    key_list.reverse()
    decrypted_hex, decrypted_text = ecb_algorithm(C, key_list)
    print('\n\nDecrypted hex:', decrypted_hex)
    print('Decrypted text:', decrypted_text)


def decrypt_cbc(text, key):
    """Decryption from hex to original text"""

    c_previous = '0000000000000001'
    result_hex, result_text = [], []

    # Convert encrypted hex to 64-bit blocks
    text = wrap(text, 16)
    C = convert_hex_to_bin(text)

    key_list = prepare_key(key)
    key_list.reverse()

    for i in C:
        decrypted_hex, decrypted_text = ecb_algorithm([i], key_list)

        decrypted_dec = int(decrypted_hex, 16)
        decrypted = decrypted_dec ^ int(c_previous, 2)
        c_previous = bin(decrypted_dec)[2:]

        decrypted_text = convert_bin_to_text(bin(decrypted)[2:].zfill(64))

        result_hex.append(hex(decrypted)[2:].zfill(16))
        result_text.append(decrypted_text)

    print('\n\nDecrypted hex:', ''.join(result_hex))
    print('Decrypted text:', ''.join(result_text))


def decrypt_3des(text, key):
    """Decryption from hex to original text"""

    keys = [key, "big", "smoke"]
    decrypted_hex = text

    for i in range(3):
        key_list = prepare_key(keys[2-i])
        key_list.reverse()

        # Convert encrypted hex to 64-bit blocks
        decrypted_hex = wrap(decrypted_hex, 16)
        C = convert_hex_to_bin(decrypted_hex)

        decrypted_hex, decrypted_text = ecb_algorithm(C, key_list)

    print('\n\nDecrypted hex:', decrypted_hex)
    print('Decrypted text:', decrypted_text)


def encrypt_ecb(text, key):
    """Encryption original text to hex des-ecb"""

    # Convert source text to 64-bit blocks
    T = convert_text_to_64(text)
    print('\nT: ', T)

    key_list = prepare_key(key)
    encrypted_hex, encrypted_text = ecb_algorithm(T, key_list)
    print('\n\nEncrypted hex:', encrypted_hex)
    print('Encrypted text:', encrypted_text)


def encrypt_cbc(text, key):
    """Encryption original text to hex des-cbc"""

    C = '0000000000000001'
    key_list = prepare_key(key)
    result_hex,  result_text = [], []

    # Convert source text to 64-bit blocks
    T = convert_text_to_64(text)
    print('\nT: ', T)

    for i in T:
        # XOR C and T
        C = bin(int(C, 2) ^ int(i, 2))[2:].zfill(64)

        encrypted_hex, encrypted_text = ecb_algorithm([C], key_list)
        result_hex.append(encrypted_hex)
        result_text.append(encrypted_text)

    print('\n\nEncrypted hex:', ''.join(result_hex))
    print('Encrypted text:', ''.join(result_text))


def encrypt_des_eee3(text, key):
    """Encryption original text to hex des-eee3"""

    keys = [key, "big", "smoke"]
    input_hex = convert_text_to_64(text)

    for i in range(3):
        key_list = prepare_key(keys[i])
        encrypted_hex, encrypted_text = ecb_algorithm(input_hex, key_list)
        input_hex = wrap(encrypted_hex, 16)
        input_hex = convert_hex_to_bin(input_hex)

    print('\n\nEncrypted hex:', encrypted_hex)
    print('Encrypted text:', encrypted_text)


def des(text, key, mode, des_type):
    if mode == 1:
        if des_type == 1:
            encrypt_ecb(text, key)
        if des_type == 2:
            encrypt_cbc(text, key)
        if des_type == 3:
            encrypt_des_eee3(text, key)
        if des_type == 4:
            pass
        if des_type == 5:
            pass

    if mode == 2:
        if des_type == 1:
            decrypt_ecb(text, key)
        if des_type == 2:
            decrypt_cbc(text, key)
        if des_type == 3:
            decrypt_3des(text, key)


if __name__ == '__main__':

    while True:
        text = input('\nInput text/hex: ')
        key = input('Input key: ')
        mode = int(input('Input mode (1 - encrypt, 2 - decrypt): '))
        print('(1 - DES-ECB, 2 - DES-CBC, 3 - DES-EEE3, 4 - DES-EDE3, 5 - DES-EEE2)')
        des_type = int(input('''Choose des type: '''))
        des(text, key, mode, des_type)

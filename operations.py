import numpy as np
from functools import reduce


def save_text(text, path):
    with open(path, mode="wb") as file:
        file.write(text)


def load_text(path):
    with open(path, mode="rb") as file:
        return file.read()


def text_to_bits(text, encoding="utf-8", errors="surrogatepass"):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def btext_to_bits(text, encoding="utf-8", errors="surrogatepass"):
    bits = bin(int.from_bytes(text, 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def btext_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big') or '\0'


def has_unique_rows(array):
    res = True
    for row in array:
        res = res and len(np.unique(row)) == len(row)

    return res


def main():
    test_message = '1234567891230458'

    a = text_to_bits(test_message)
    print('1', a, "  len = ", len(a))
    print(int(a, 2))
    print('2', text_from_bits(a))

    a = np.uint8(2)
    print(a, type(a))


if __name__ == "__main__":
    main()

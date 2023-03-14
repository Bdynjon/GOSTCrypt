import numpy as np
from functools import reduce


def text_to_bits(text, encoding="utf-8", errors="surrogatepass"):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def encode_string(string: str):
    array = map(text_to_bits, string)
    array = list(reduce(lambda res, el: res+el, array))
    size = len(array)
    size_code = list(bin(size)[2:].zfill(15))

    return size_code + array


def decode_string(array):
    size_text = "".join(array[:15])
    size = int("0b" + size_text[::-1], 2)

    bits_string = "".join(array[15:])
    text = ""
    for i in range(8, size+8, 8):
        try:
            text += text_from_bits(bits_string[i-8:i])
        except:
            continue

    return text


def main():
    pass


if __name__ == "__main__":
    main()

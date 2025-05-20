def my_pow(base, exp, mod):
    if exp < 0:
        raise ValueError
    if exp == 0:
        return 1

    accumulator = my_pow((base * base) % mod, exp >> 1, mod)
    if exp % 2 == 0:
        return accumulator
    else:
        return (base * accumulator) % mod


def main():
    assert my_pow(17, 5, 7) == pow(17, 5, 7)


if __name__ == "__main__":
    main()

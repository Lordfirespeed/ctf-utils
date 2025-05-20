from extras.math_extras.factorise.pollards_rho import make_pollards_rho_factoriser


factoriser = make_pollards_rho_factoriser(seed=1)


def main():
    value = 7171
    factor = factoriser(value)
    print(f"{factor = }, {divmod(value, factor) = }")


if __name__ == "__main__":
    main()

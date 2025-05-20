from extras.math_extras.factorise.pollards_p_minus_1 import pollards_p_minus_1_factorise
from extras.math_extras.factorise.hybrid import prime_factorise


def main():
    # the minimum smoothness bound can be found by binary search
    value = 15770708441
    factor = pollards_p_minus_1_factorise(value, 173)
    print(f"{factor = }, {divmod(value, factor) = }")

    # alternatively, we can do something cleverer: the minimum smoothness bound will be
    # the largest prime power factor of p-1 (aka the minimum n s.t. p-1 is n-powersmooth)
    factor = pollards_p_minus_1_factorise(value, 10_000)
    p_minus_1_factorisation = prime_factorise(factor - 1)
    p_minus_1_prime_power_factors = (pow(p, c) for p, c in p_minus_1_factorisation.items())
    largest_prime_power_factor_of_p_minus_1 = max(p_minus_1_prime_power_factors)
    print(f"{largest_prime_power_factor_of_p_minus_1 = }")


if __name__ == "__main__":
    main()

"""
https://gist.github.com/nakov/60d62bdf4067ea72b7832ce9f71ae079
"""
from operator import index
from typing import SupportsIndex


def legendre_symbol(n: int, mod: int) -> int:
    """
    Compute the Legendre symbol n|p using Euler's criterion.
    p is a prime, n is relatively prime to p (if p divides n, then n|p = 0)

    Returns True if n has a square root modulo p, False otherwise.
    """
    ls = pow(n, (mod - 1) // 2, mod)
    return ls != mod - 1


def mod_sqrt(n: SupportsIndex, mod: SupportsIndex) -> int:
    """
    Find a quadratic residue (mod p) of 'n'. p must be an odd prime.

    Solve the congruence of the form:
        x^2 = n (mod p)
    And returns x. Note that p - x is also a root.

    Returns 0 if no square root exists.

    The Tonelli-Shanks algorithm is used (except for some simple cases in which the solution is known from an identity).
    This algorithm runs in polynomial time (unless the generalized Riemann hypothesis is false).
    """
    n = index(n)
    mod = index(mod)

    # Simple cases
    #
    if not legendre_symbol(n, mod):
        return 0
    elif n == 0:
        return 0
    elif mod == 2:
        return mod
    elif mod % 4 == 3:
        return pow(n, (mod + 1) // 4, mod)

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = mod - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    # Find some 'a' with a legendre symbol a|p = -1.
    # Shouldn't take long.
    #
    a = 2
    while legendre_symbol(a, mod):
        a += 1

    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #

    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    x = pow(n, (s + 1) // 2, mod)
    b = pow(n, s, mod)
    g = pow(a, s, mod)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, mod)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), mod)
        g = (gs * gs) % mod
        x = (x * gs) % mod
        b = (b * g) % mod
        r = m


__all__ = ("mod_sqrt",)


def main():
    assert mod_sqrt(223, 17) == 6


if __name__ == "__main__":
    main()

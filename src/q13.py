from extras.math_extras.elliptic_curve import *

curve = Curve(p=16001, a=1, b=5)
g = AffinePoint(1300, 16000)

d_alice = 125
d_bob = 13333

q_alice = curve.scalar_mul_affine_point(d_alice, g)
q_bob = curve.scalar_mul_affine_point(d_bob, g)

k_alice = curve.scalar_mul_affine_point(d_alice, q_bob)
k_bob = curve.scalar_mul_affine_point(d_bob, q_alice)

shared_secret = k_alice.x

def main():
    print(f"{d_alice = }")
    print(f"{d_bob = }")
    print(f"{q_alice = }")
    print(f"{q_bob = }")
    print(f"{k_alice = }")
    print(f"{k_bob = }")


if __name__ == "__main__":
    main()

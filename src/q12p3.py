from extras.math_extras.elliptic_curve import *


def main():
    curve = Curve(p=29, a=4, b=20)
    g = AffinePoint(0, 7)
    index = 0
    while True:
        point = curve.scalar_mul_affine_point(index, g)
        if index > 0 and point.is_at_infinity():
            break
        print(index, point)
        index += 1


if __name__ == "__main__":
    main()

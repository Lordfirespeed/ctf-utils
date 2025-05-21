from extras.math_extras.elliptic_curve import *


def main():
    curve = Curve(p=7, a=1, b=1)
    points = set(curve.all_affine_points_by_exhaustion())
    # all points are generators when field has prime order
    generators = (point for point in points if not point.is_at_infinity())
    generator = next(generators)
    generated_points = list(curve.scalar_mul_affine_point(k, generator) for k in range(len(points)))
    assert points == set(generated_points)

    print(f"{'':>25}" + "".join(f"{point!s:^25}" for point in generated_points))
    for point_1 in generated_points:
        print(f"{point_1!s:>25}" + "".join(f"{curve.add_affine_points(point_1, point_2)!s:^25}" for point_2 in generated_points))


if __name__ == "__main__":
    main()

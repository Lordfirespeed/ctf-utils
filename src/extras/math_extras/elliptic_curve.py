from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from math import lcm
from typing import Generator

from extras.math_extras.mod_sqrt import mod_sqrt


class PointABC(metaclass=ABCMeta):
    @abstractmethod
    def is_at_infinity(self) -> bool: ...


class AffinePointABC(PointABC, metaclass=ABCMeta):
    pass


class JacobianPointABC(PointABC, metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class AffinePoint(AffinePointABC):
    __slots__ = ("x", "y")

    x: int
    y: int

    def is_at_infinity(self) -> bool:
        return False

    def __str__(self):
        return f"({self.x}, {self.y})"


@dataclass(frozen=True)
class AffinePointAtInfinityType(AffinePointABC):
    __slots__ = tuple()

    def is_at_infinity(self) -> bool:
        return True

    def __repr__(self):
        return "AffinePointAtInfinity"

    def __str__(self):
        return "inf"


AffinePointAtInfinity = AffinePointAtInfinityType()


@dataclass(frozen=True)
class JacobianPoint(JacobianPointABC):
    __slots__ = ("x", "y", "z")

    x: int
    y: int
    z: int

    def is_at_infinity(self) -> bool:
        return self.z == 0

    def __str__(self):
        return f"({self.x}, {self.y})"


type Point = AffinePointABC | JacobianPointABC


@dataclass(frozen=True)
class Curve:
    __slots__ = ("p", "a", "b")

    p: int  # prime field order and modulus for operations
    a: int  # coefficient in Weierstrass equation
    b: int  # coefficient in Weierstrass equation

    def all_affine_points_by_exhaustion(self) -> Generator[AffinePointABC]:
        yield AffinePointAtInfinity
        for x in range(self.p):
            yy = (pow(x, 3, mod=self.p) + (self.a * x) + self.b) % self.p
            y = mod_sqrt(yy, self.p)
            if y == 0:
                continue
            yield AffinePoint(x, y)
            yield AffinePoint(x, self.p - y)

    def to_jacobian(self, affine: AffinePointABC) -> JacobianPointABC:
        if affine.is_at_infinity():
            return JacobianPoint(1, 1, 0)
        if isinstance(affine, AffinePoint):
            return JacobianPoint(affine.x, affine.y, 1)
        raise ValueError

    def to_affine(self, jacobian: JacobianPointABC) -> AffinePointABC:
        if jacobian.is_at_infinity():
            return AffinePointAtInfinity
        if isinstance(jacobian, JacobianPoint):
            inv_z = pow(jacobian.z, -1, self.p)
            affine_x = (jacobian.x * pow(inv_z, 2, mod=self.p)) % self.p
            affine_y = (jacobian.y * pow(inv_z, 3, mod=self.p)) % self.p
            return AffinePoint(affine_x, affine_y)
        raise ValueError

    def is_jacobian_point_on_curve(self, point: JacobianPointABC) -> bool:
        if point.is_at_infinity():
            return True
        if not isinstance(point, JacobianPoint): raise ValueError
        left_side = pow(point.y, 2, mod=self.p)
        right_side = (pow(point.x, 3, mod=self.p) + (self.a * point.x * pow(point.z, 4, mod=self.p)) + (self.b * pow(point.z, 6, mod=self.p))) % self.p
        return left_side == right_side

    def is_affine_point_on_curve(self, point: AffinePointABC) -> bool:
        if point.is_at_infinity():
            return True
        if not isinstance(point, AffinePoint): raise ValueError
        left_side = pow(point.y, 2, mod=self.p)
        right_side = (pow(point.x, 3, mod=self.p) + (self.a * point.x) + self.b) % self.p
        return left_side == right_side

    def is_point_on_curve(self, point: Point) -> bool:
        if isinstance(point, AffinePointABC):
            return self.is_affine_point_on_curve(point)
        if isinstance(point, JacobianPointABC):
            return self.is_jacobian_point_on_curve(point)

        raise ValueError

    def scale_z_jacobian_point(self, a: int, p: JacobianPointABC) -> JacobianPointABC:
        if p.is_at_infinity():
            return p
        if not isinstance(p, JacobianPoint):
            raise ValueError

        # https://www.hyperelliptic.org/EFD/g1p/auto-shortw-jacobian.html#scaling-z
        aa = pow(a, 2, mod=self.p)
        x3 = (p.x * aa) % self.p
        y3 = (p.y * aa * a) % self.p
        z3 = (p.z * a) % self.p
        return JacobianPoint(x3, y3, z3)

    def unit_z_jacobian_point(self, p: JacobianPointABC) -> JacobianPointABC:
        if p.is_at_infinity():
            return p
        if not isinstance(p, JacobianPoint):
            raise ValueError

        a = pow(p.z, -1, mod=self.p)
        return self.scale_z_jacobian_point(a, p)

    def eq_jacobian_points(self, p1: JacobianPointABC, p2: JacobianPointABC) -> bool:
        if p1.is_at_infinity() and p2.is_at_infinity():
            return True
        if p1.is_at_infinity() or p2.is_at_infinity():
            return False

        if not isinstance(p1, JacobianPoint):
            raise ValueError
        if not isinstance(p2, JacobianPoint):
            raise ValueError

        if p1.z == p2.z:
            return p1.x == p2.x and p1.y == p2.y

        z_lcm = lcm(p1.z, p2.z)
        p1_scale = z_lcm // p1.z
        p2_scale = z_lcm // p2.z
        p1_scaled = self.scale_z_jacobian_point(p1_scale, p1)
        p2_scaled = self.scale_z_jacobian_point(p2_scale, p2)
        assert isinstance(p1_scaled, JacobianPoint)
        assert isinstance(p2_scaled, JacobianPoint)
        assert p1_scaled.z == p2_scaled.z
        return p1_scaled.x == p2_scaled.x and p1_scaled.y == p2_scaled.y

    def double_affine_point(self, p: AffinePointABC) -> AffinePointABC:
        if p.is_at_infinity():
            return AffinePointAtInfinity

        if not isinstance(p, AffinePoint):
            raise ValueError

        p_jacobian = self.to_jacobian(p)
        q_jacobian = self.double_jacobian_point(p_jacobian)
        return self.to_affine(q_jacobian)

    def double_jacobian_point(self, p: JacobianPointABC) -> JacobianPointABC:
        if p.is_at_infinity():
            return p

        if not isinstance(p, JacobianPoint):
            raise ValueError

        # https://www.hyperelliptic.org/EFD/g1p/auto-shortw-jacobian.html#doubling-dbl-2007-bl
        xx = pow(p.x, 2, mod=self.p)
        yy = pow(p.y, 2, mod=self.p)
        yyyy = pow(yy, 2, mod=self.p)
        zz = pow(p.z, 2, mod=self.p)
        s = (2 * (pow(p.x + yy, 2, mod=self.p) - xx - yyyy)) % self.p
        m = (3 * xx + self.a * pow(zz, 2, mod=self.p)) % self.p
        t = (pow(m, 2, mod=self.p) - 2 * s) % self.p
        x3 = t
        y3 = (m * (s - t) - 8 * yyyy) % self.p
        z3 = (pow(p.y + p.z, 2, mod=self.p) - yy - zz) % self.p

        return JacobianPoint(x3, y3, z3)

    def add_affine_points(self, p1: AffinePointABC, p2: AffinePointABC) -> AffinePointABC:
        if p1.is_at_infinity():
            return p2
        if p2.is_at_infinity():
            return p1

        if not isinstance(p1, AffinePoint):
            raise ValueError
        if not isinstance(p2, AffinePoint):
            raise ValueError

        p1_jacobian = self.to_jacobian(p1)
        p2_jacobian = self.to_jacobian(p2)
        q_jacobian = self.add_jacobian_points(p1_jacobian, p2_jacobian)
        return self.to_affine(q_jacobian)

    def add_jacobian_points(self, p1: JacobianPointABC, p2: JacobianPointABC) -> JacobianPointABC:
        if p1.is_at_infinity():
            return p2
        if p2.is_at_infinity():
            return p1

        if self.eq_jacobian_points(p1, p2):
            return self.double_jacobian_point(p1)

        if not isinstance(p1, JacobianPoint):
            raise ValueError
        if not isinstance(p2, JacobianPoint):
            raise ValueError

        # https://www.hyperelliptic.org/EFD/g1p/auto-shortw-jacobian.html#addition-add-2007-bl
        z1z1 = pow(p1.z, 2, mod=self.p)
        z2z2 = pow(p2.z, 2, mod=self.p)
        u1 = (p1.x * z2z2) % self.p
        u2 = (p2.x * z1z1) % self.p
        s1 = (p1.y * p2.z * z2z2) % self.p
        s2 = (p2.y * p1.z * z1z1) % self.p
        h = (u2 - u1) % self.p
        i = pow(2 * h, 2, mod=self.p)
        j = (h * i) % self.p
        r = (2 * (s2 - s1)) % self.p
        v = (u1 * i) % self.p
        x3 = (pow(r, 2, mod=self.p) - j - (2 * v)) % self.p
        y3 = (r * (v - x3) - (2 * s1 * j)) % self.p
        z3 = ((pow(p1.z + p2.z, 2, mod=self.p) - z1z1 - z2z2) * h) % self.p

        return JacobianPoint(x3, y3, z3)

    def scalar_mul_affine_point(self, k: int, p: AffinePointABC) -> AffinePointABC:
        if p.is_at_infinity():
            return AffinePointAtInfinity
        if k < 0:
            raise ValueError
        if k == 0:
            return AffinePointAtInfinity

        p_jacobian = self.to_jacobian(p)
        q_jacobian = self.scalar_mul_jacobian_point(k, p_jacobian)
        return self.to_affine(q_jacobian)

    def scalar_mul_jacobian_point(self, k: int, p: JacobianPointABC) -> JacobianPointABC:
        if p.is_at_infinity():
            return p
        if k < 0:
            raise ValueError
        if k == 0:
            return JacobianPoint(1, 1, 0)

        accumulator = self.scalar_mul_jacobian_point(k >> 1, self.double_jacobian_point(p))
        if k % 2 == 0:
            return accumulator
        else:
            return self.add_jacobian_points(p, accumulator)


__all__ = (
    "PointABC",
    "AffinePointABC",
    "JacobianPointABC",
    "AffinePoint",
    "AffinePointAtInfinity",
    "JacobianPoint",
    "Point",
    "Curve",
)

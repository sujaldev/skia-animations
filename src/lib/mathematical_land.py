from math import sqrt, sin, cos, pi
from skia import Canvas, Color, Paint
import numpy as np
from scipy.linalg import expm, norm


class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    @property
    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    @property
    def xy(self):
        return self.x, self.y

    @property
    def xyz(self):
        return self.x, self.y, self.z

    def scale(self, scalar):
        scaled = Vector(self.x, self.y, self.z)
        scaled.x *= scalar
        scaled.y *= scalar
        scaled.z *= scalar
        return scaled

    def len(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __add__(self, other):
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other):
        return Vector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __mul__(self, other):
        return Vector(*np.cross(
            np.array(self.xyz),
            np.array(other.xyz)
        ))

    def __truediv__(self, other):
        if type(other) == Vector:
            return Vector(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return Vector(self.x / other, self.y / other, self.z / other)

    def __repr__(self):
        return f"Vec({self.x}, {self.y}, {self.z})"


class Square3D:
    def __init__(self, top_left: Vector, x_rotation: float, y_rotation: float, side: float):
        self.top_left = top_left
        self.x_rotation = float(x_rotation)
        self.y_rotation = float(y_rotation)
        self.side = float(side)

    @property
    def top_right(self) -> Vector:
        return self.top_left + Vector(x=self.side * cos(self.y_rotation), z=self.side * sin(self.y_rotation))

    @property
    def bottom_left(self) -> Vector:
        partial_length = self.side * sin(self.x_rotation)
        return self.top_left + Vector(
            y=self.side * cos(self.x_rotation),
            x=-partial_length * sin(self.y_rotation),
            z=-partial_length * cos(self.y_rotation)
        )

    @property
    def bottom_right(self) -> Vector:
        partial_length = self.side * sin(self.x_rotation)
        return self.top_right + Vector(
            y=self.side * cos(self.x_rotation),
            x=-partial_length * sin(self.y_rotation),
            z=-partial_length * cos(self.y_rotation)
        )

    @property
    def points(self) -> tuple:
        return (
            self.top_left,
            self.top_right,
            self.bottom_right,
            self.bottom_left
        )

    def paint(self, canvas: Canvas, stroke_width: float, stroke_color: Color):
        points = self.points
        paint = Paint(
            Color=stroke_color,
            StrokeWidth=stroke_width
        )
        for i in range(len(points)):
            canvas.drawLine(
                *points[i].xy,
                *points[(i + 1) % len(points)].xy,
                paint
            )

    def __repr__(self):
        return f"[Origin: {self.top_left}," \
               f" Top Right: {self.top_right}," \
               f" Bottom Left: {self.bottom_left}," \
               f" Bottom Right: {self.bottom_right}]"


class Cube:
    def __init__(self, front_top_left: Vector, x_rotation: float, y_rotation: float, side: float):
        self.front_top_left = front_top_left
        self.x_rotation = float(x_rotation)
        self.y_rotation = float(y_rotation)
        self.side = side

    @property
    def front_plane(self) -> Square3D:
        return Square3D(self.front_top_left, self.x_rotation, self.y_rotation, self.side)

    @property
    def back_plane(self) -> Square3D:
        front_top_left = self.front_top_left - Vector(
            y=-self.side * sin(self.x_rotation),
            x=-self.side * cos(self.x_rotation) * sin(self.y_rotation),
            z=-self.side * cos(self.x_rotation) * cos(self.y_rotation),
        )
        return Square3D(front_top_left, self.x_rotation, self.y_rotation, self.side)

    @property
    def plane_joining_points(self):
        return (
            (self.front_plane.top_left, self.back_plane.top_left),
            (self.front_plane.top_right, self.back_plane.top_right),
            (self.front_plane.bottom_right, self.back_plane.bottom_right),
            (self.front_plane.bottom_left, self.back_plane.bottom_left),
        )

    def paint(self, canvas: Canvas, stroke_width: float, stroke_color: Color):
        self.front_plane.paint(canvas, stroke_width, stroke_color)
        self.back_plane.paint(canvas, stroke_width, stroke_color)
        paint = Paint(
            Color=stroke_color,
            StrokeWidth=stroke_width
        )
        for p1, p2 in self.plane_joining_points:
            canvas.drawLine(p1.xy, p2.xy, paint)
    #
    # @property
    # def p1(self):
    #     return self.front_top_left
    #
    # @property
    # def p2(self):
    #     return self.front_plane.top_right
    #
    # @property
    # def p3(self):
    #     return self.front_plane.bottom_right
    #
    # @property
    # def p4(self):
    #     return self.front_plane.bottom_right
    #
    # @property
    # def p5(self):
    #     return self.back_plane.top_left
    #
    # @property
    # def p6(self):
    #     return self.back_plane.top_right
    #
    # @property
    # def p7(self):
    #     return self.back_plane.bottom_right
    #
    # @property
    # def p8(self):
    #     return self.back_plane.bottom_right


class Circle:
    def __init__(self, origin: Vector, radius: float, x_rotation: float = 0, z_rotation: float = 0):
        self.origin = origin
        self.radius = radius
        self.x_rotation = x_rotation
        self.z_rotation = z_rotation

    @property
    def normal(self) -> Vector:
        # Returns a unit vector in the direction perpendicular to the plane in which the circle lies.
        normal = Vector()
        normal.z = sin(self.x_rotation)
        normal.y = -cos(self.x_rotation)
        normal.z = normal.z * cos(self.z_rotation)
        normal.x = normal.z * sin(self.z_rotation)
        return normal

    @property
    def radius_line(self) -> Vector:
        # Returns a unit in the direction parallel to the plane in which the circle lies
        perpendicular_vector = self.origin * self.normal
        unit_vector = perpendicular_vector / perpendicular_vector.len()
        return unit_vector.scale(self.radius)

    @staticmethod
    def rotate(vector: Vector, axis: Vector, theta: float):
        # https://stackoverflow.com/a/25709323/15007549
        vector = np.array(vector.xyz)
        axis = np.array(axis.xyz)
        m0 = expm(np.cross(np.eye(3), axis / norm(axis) * theta))
        return Vector(*np.dot(m0, vector))

    def paint(self, canvas: Canvas, stroke_width: float, stroke_color: Color):
        resolution = 100
        step = (2 * pi) / resolution
        angle = step
        radius_line = self.radius_line
        normal = self.normal
        paint = Paint(Color=stroke_color, StrokeWidth=stroke_width)
        for i in range(resolution):
            next_angle = angle + step
            p1 = self.origin + self.rotate(radius_line, normal, angle)
            p2 = self.origin + self.rotate(radius_line, normal, next_angle)
            canvas.drawLine(p1.xy, p2.xy, paint)
            angle += step

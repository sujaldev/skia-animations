from lib.mathematical_land import Square3D, Cube, Vector
from skia import Canvas, Color, Paint
from lib.ui_backend import Window


def calc_point_projection(point: Vector, eye: Vector):
    x, y, z = point.x, point.y, point.z
    x_e, y_e, z_e = eye.x, eye.y, eye.z
    projected_y = y + ((z * (y_e - y)) / (z - z_e))
    projected_x = x + ((z * (x_e - x)) / (z - z_e))
    return Vector(
        projected_x, projected_y, 0
    )


class PerspectiveSquare3D(Square3D):
    def __init__(self, eye: Vector, top_left: Vector, x_rotation: float, y_rotation: float, side: float):
        self.eye = eye
        super().__init__(top_left, x_rotation, y_rotation, side)

    def paint(self, canvas: Canvas, stroke_width: float, stroke_color: Color):
        points = self.points
        paint = Paint(
            Color=stroke_color,
            StrokeWidth=stroke_width
        )
        for i in range(len(points)):
            canvas.drawLine(
                *calc_point_projection(points[i], self.eye).xy,
                *calc_point_projection(points[(i + 1) % len(points)], self.eye).xy,
                paint
            )


class PerspectiveCube(Cube):
    def __init__(self, eye: Vector, front_top_left: Vector, x_rotation: float, y_rotation: float, side: float):
        self.eye = eye
        super().__init__(front_top_left, x_rotation, y_rotation, side)

    @property
    def front_plane(self) -> Square3D:
        square = super().front_plane
        return PerspectiveSquare3D(
            self.eye, square.top_left, square.x_rotation, self.y_rotation, square.side
        )

    @property
    def back_plane(self) -> Square3D:
        square = super().back_plane
        return PerspectiveSquare3D(
            self.eye, square.top_left, square.x_rotation, self.y_rotation, square.side
        )

    def paint(self, canvas: Canvas, stroke_width: float, stroke_color: Color):
        self.front_plane.paint(canvas, stroke_width, stroke_color)
        self.back_plane.paint(canvas, stroke_width, stroke_color)
        paint = Paint(
            Color=stroke_color,
            StrokeWidth=stroke_width
        )
        for p1, p2 in self.plane_joining_points:
            canvas.drawLine(
                *calc_point_projection(p1, self.eye).xy,
                *calc_point_projection(p2, self.eye).xy,
                paint
            )


main_cube = PerspectiveCube(
    Vector(500, 500, -100),
    Vector(500, 500, 0),
    0, 0, 200
)


def event_loop(canvas: Canvas, event):
    canvas.drawColor(Color(0, 0, 0))

    if event.window.data1 == 79:
        main_cube.y_rotation += .05
    elif event.window.data1 == 80:
        main_cube.y_rotation -= .05
    elif event.window.data1 == 82:
        main_cube.x_rotation += .05
    elif event.window.data1 == 81:
        main_cube.x_rotation -= .05

    main_cube.paint(canvas, 3, Color(0, 255, 0))


window = Window("Perspective Cube", 1000, 1000, event_loop=event_loop)
window.start()

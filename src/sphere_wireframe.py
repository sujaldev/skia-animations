from lib.mathematical_land import SphereWireframe, Vector
from lib.ui_backend import Window
from skia import Canvas, Color

sphere = SphereWireframe(
    Vector(910, 490, 0),
    200, 0, 0, 20
)


def event_loop(canvas: Canvas, event):
    canvas.drawColor(Color(25, 25, 25))

    if event.window.data1 == 79:
        sphere.y_rotation += .05
    elif event.window.data1 == 80:
        sphere.y_rotation -= .05
    elif event.window.data1 == 82:
        sphere.x_rotation += .05
    elif event.window.data1 == 81:
        sphere.x_rotation -= .05

    sphere.paint(canvas, 1, Color(0, 150, 150))


window = Window("Simple Ring", 1920, 1080, event_loop=event_loop)
window.start()

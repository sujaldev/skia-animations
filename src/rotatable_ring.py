from lib.mathematical_land import Circle, Vector
from lib.ui_backend import Window
from skia import Canvas, Color

ring = Circle(
    Vector(910, 490, 0),
    100, 0, 0
)


def event_loop(canvas: Canvas, event):
    canvas.drawColor(Color(25, 25, 25))

    if event.window.data1 == 79:
        ring.y_rotation += .05
    elif event.window.data1 == 80:
        ring.y_rotation -= .05
    elif event.window.data1 == 82:
        ring.x_rotation += .05
    elif event.window.data1 == 81:
        ring.x_rotation -= .05

    ring.paint(canvas, 3, Color(0, 255, 0))


window = Window("Simple Ring", 1920, 1080, event_loop=event_loop)
window.start()

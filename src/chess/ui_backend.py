import math
from ctypes import byref as pointer
from time import time, sleep

import sdl2 as sdl
import skia

canvas_color = (40, 40, 40)
fps = 60


class Window:
    DEFAULT_FLAGS = sdl.SDL_WINDOW_SHOWN | sdl.SDL_WINDOW_RESIZABLE
    BYTE_ORDER = {
        # ---------- ->   RED        GREEN       BLUE        ALPHA
        "BIG_ENDIAN": (0xff000000, 0x00ff0000, 0x0000ff00, 0x000000ff),
        "LIL_ENDIAN": (0x000000ff, 0x0000ff00, 0x00ff0000, 0xff000000)
    }

    PIXEL_DEPTH = 32  # BITS PER PIXEL
    PIXEL_PITCH_FACTOR = 4  # Multiplied by Width to get BYTES PER ROW

    def __init__(self, title, width, height, x=None, y=None, flags=None):
        self.title = bytes(title, "utf8")
        self.width = width
        self.height = height
        self.frame_renderer = None

        self.canvas_color = canvas_color

        # Center Window By default
        self.x, self.y = x, y
        if x is None:
            self.x = sdl.SDL_WINDOWPOS_CENTERED
        if y is None:
            self.y = sdl.SDL_WINDOWPOS_CENTERED

        # Override flags
        if flags is None:
            self.flags = self.DEFAULT_FLAGS
        else:
            self.flags = flags

        # SET RGBA MASKS BASED ON BYTE_ORDER
        is_big_endian = sdl.SDL_BYTEORDER == sdl.SDL_BIG_ENDIAN
        self.RGBA_MASKS = self.BYTE_ORDER["BIG_ENDIAN" if is_big_endian else "LIL_ENDIAN"]

        # CALCULATE PIXEL PITCH
        self.PIXEL_PITCH = self.PIXEL_PITCH_FACTOR * self.width

        # SKIA INIT
        self.skia_surface = self.__create_skia_surface()
        # Creating a member variable because SDL_CreateRGBSurfaceFrom does not keep pixel data but a pointer to it,
        # so if it were to be a local variable it'd go out of scope and be deleted by the python garbage collector.
        self.skia_pixel_data = None

        # SDL INIT
        sdl.SDL_Init(sdl.SDL_INIT_EVENTS)  # INITIALIZE SDL EVENTS
        self.sdl_window = self.__create_SDL_Window()

    def __create_SDL_Window(self):
        window = sdl.SDL_CreateWindow(
            self.title,
            self.x, self.y,
            self.width, self.height,
            self.flags
        )
        return window

    def __create_skia_surface(self):
        """
        Initializes the main skia surface that will be drawn upon,
        creates a raster surface.
        """
        self.PIXEL_PITCH = self.PIXEL_PITCH_FACTOR * self.width
        surface_blueprint = skia.ImageInfo.Make(
            self.width, self.height,
            ct=skia.kRGBA_8888_ColorType,
            at=skia.kUnpremul_AlphaType
        )
        # noinspection PyArgumentList
        surface = skia.Surface.MakeRaster(surface_blueprint)

        # make the canvas white by default
        with surface as canvas:
            canvas.drawColor(skia.Color(*self.canvas_color))

        return surface

    def __update_pixel_data_from_skia_surface(self):
        """
        Converts Skia Surface into a bytes object containing pixel data
        """
        image = self.skia_surface.makeImageSnapshot()
        self.skia_pixel_data = image.tobytes()

    def __transform_skia_surface_to_SDL_surface(self):
        """
        Converts Skia Surface to an SDL surface by first converting
        Skia Surface to Pixel Data using .__update_pixel_data_from_skia_surface
        """
        self.__update_pixel_data_from_skia_surface()
        sdl_surface = sdl.SDL_CreateRGBSurfaceFrom(
            self.skia_pixel_data,
            self.width, self.height,
            self.PIXEL_DEPTH, self.PIXEL_PITCH,
            *self.RGBA_MASKS
        )
        return sdl_surface

    def update(self):
        window_surface = sdl.SDL_GetWindowSurface(self.sdl_window)  # the SDL surface associated with the window
        transformed_skia_surface = self.__transform_skia_surface_to_SDL_surface()
        # Transfer skia surface to SDL window's surface
        sdl.SDL_BlitSurface(
            transformed_skia_surface, None,
            window_surface, None
        )

        # Update window with new copied data
        sdl.SDL_UpdateWindowSurface(self.sdl_window)

    def event_loop(self, event):
        while sdl.SDL_PollEvent(pointer(event)) != 0:

            window_resized = event.type == sdl.SDL_WINDOWEVENT and event.window.event == sdl.SDL_WINDOWEVENT_RESIZED
            if window_resized:
                self.handle_resize(event)

            if event.type == sdl.SDL_QUIT:
                return 0

    @staticmethod
    def cap_framerate(start, end, fps):
        frame_delta = 1 / fps
        dt = frame_delta - (end - start)
        if dt > 0:
            sleep(dt)
        return dt

    def main_loop(self):
        self.update()

        init_time = time()

        while True:
            start = time() - init_time

            # Event loop
            event = sdl.SDL_Event()
            if self.event_loop(event) == 0:
                self.handle_quit()
                return

            if self.frame_renderer:
                with self.skia_surface as canvas:
                    canvas: skia.Canvas
                    self.frame_renderer(canvas, time() - init_time)
                    self.update()

            # Frame
            end = time() - init_time
            self.cap_framerate(start, end, fps)

    def handle_resize(self, event):
        self.width = event.window.data1
        self.height = event.window.data2
        # Create a new skia surface from the updated dimensions (required so no segfaults occur)
        self.skia_surface = self.__create_skia_surface()
        self.update()

    # noinspection PyMethodMayBeStatic
    def handle_quit(self):
        sdl.SDL_Quit()
        print("Quiting...")


if __name__ == "__main__":
    skiaSDLWindow = Window("Lyn", 1000, 800, flags=sdl.SDL_WINDOW_SHOWN | sdl.SDL_WINDOW_RESIZABLE)
    skiaSDLWindow.main_loop()

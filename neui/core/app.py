import os
import sys

import glfw
import skia

from .renderer import Renderer
from .events import EventManager
from .layout import compute_layout
from .animation import animation_manager


def _env_enabled(name):
    """Return whether an environment variable enables a feature."""
    return os.environ.get(name, "").strip().casefold() in {
        "1",
        "true",
        "yes",
        "on",
    }


class App:
    _instance = None

    @classmethod
    def get_instance(cls):
        return cls._instance

    def __init__(
        self,
        title="NEUI App",
        width=800,
        height=600,
        theme="dark",
    ):
        self.debug_enabled = _env_enabled("NEUI_DEBUG")

        self.window = None
        self.context = None
        self.surface = None
        self.canvas = None
        self.root = None
        self.overlays = []
        self.renderer = None
        self.event_manager = None
        self.stencil_bits = 0
        self._glfw_initialized = False

        # PyOpenGL remains optional. Without it, NEUI requests no stencil
        # buffer and reports zero stencil bits to Skia.
        self._load_opengl_helpers()

        # Publish the instance before configuring Renderer, but roll it back
        # if any part of initialization fails.
        App._instance = self

        try:
            if not glfw.init():
                raise RuntimeError("Could not initialize GLFW")

            self._glfw_initialized = True

            glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
            glfw.window_hint(
                glfw.STENCIL_BITS,
                8 if self._gl_get_integer is not None else 0,
            )
            glfw.window_hint(glfw.SRGB_CAPABLE, glfw.TRUE)

            self.window = glfw.create_window(
                width,
                height,
                title,
                None,
                None,
            )

            if not self.window:
                raise RuntimeError("Could not create GLFW window")

            self._configure_native_window()

        except Exception:
            self._cleanup()
            raise

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def _load_opengl_helpers(self):
        """Load optional OpenGL query functions without adding a dependency."""
        self._gl_get_integer = None
        self._gl_get_string = None
        self._gl_stencil_bits_enum = None
        self._gl_vendor_enum = None
        self._gl_renderer_enum = None
        self._gl_version_enum = None

        try:
            from OpenGL.GL import (
                GL_RENDERER,
                GL_STENCIL_BITS,
                GL_VENDOR,
                GL_VERSION,
                glGetIntegerv,
                glGetString,
            )
        except ImportError:
            return

        self._gl_get_integer = glGetIntegerv
        self._gl_get_string = glGetString
        self._gl_stencil_bits_enum = GL_STENCIL_BITS
        self._gl_vendor_enum = GL_VENDOR
        self._gl_renderer_enum = GL_RENDERER
        self._gl_version_enum = GL_VERSION

    def _debug_log(self, message):
        if self.debug_enabled:
            print(f"[NEUI] {message}", flush=True)

    @staticmethod
    def _decode_gl_string(value):
        if value is None:
            return "Unavailable"

        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")

        return str(value)

    def _print_opengl_info(self):
        """Print OpenGL information when the optional PyOpenGL is available."""
        if not self.debug_enabled:
            return

        if self._gl_get_string is None:
            self._debug_log(
                "PyOpenGL is not installed; OpenGL diagnostics skipped."
            )
            return

        try:
            self._debug_log(
                "OpenGL Vendor: "
                f"{self._decode_gl_string(self._gl_get_string(self._gl_vendor_enum))}"
            )
            self._debug_log(
                "OpenGL Renderer: "
                f"{self._decode_gl_string(self._gl_get_string(self._gl_renderer_enum))}"
            )
            self._debug_log(
                "OpenGL Version: "
                f"{self._decode_gl_string(self._gl_get_string(self._gl_version_enum))}"
            )
        except Exception as error:
            self._debug_log(
                f"Could not retrieve OpenGL information: {error}"
            )

    def _query_stencil_bits(self):
        """Return a stencil bit count supported by Skia's GL render target."""
        if self._gl_get_integer is None:
            self._debug_log(
                "PyOpenGL is unavailable; stencil buffer requested disabled."
            )
            return 0

        try:
            actual_bits = int(
                self._gl_get_integer(self._gl_stencil_bits_enum)
            )
        except Exception as error:
            raise RuntimeError(
                "Could not query the default framebuffer stencil bits"
            ) from error

        # Skia's GrBackendRenderTarget GL wrapper accepts 0, 8 or 16 stencil
        # bits. Treat any other value as unavailable to Skia.
        if actual_bits not in (0, 8, 16):
            self._debug_log(
                "Framebuffer reports an unsupported stencil size "
                f"({actual_bits} bits); disabling stencil use in Skia."
            )
            return 0

        self._debug_log(f"Framebuffer stencil bits: {actual_bits}")
        return actual_bits

    # ---------------------------------------------------------
    # Native window configuration
    # ---------------------------------------------------------

    def _configure_windows_titlebar(self):
        if sys.platform != "win32":
            return

        try:
            from ctypes import byref, c_int, windll

            hwnd = glfw.get_win32_window(self.window)
            dwm_attribute = 20

            windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                dwm_attribute,
                byref(c_int(1)),
                4,
            )
        except Exception as error:
            self._debug_log(
                f"Failed to configure Windows dark title bar: {error}"
            )

    def _configure_window_icon(self):
        try:
            if (
                sys.platform.startswith("linux")
                and glfw.get_platform() == glfw.PLATFORM_WAYLAND
            ):
                self._debug_log(
                    "Skipping GLFW window icon on Wayland. "
                    "Use desktop entry metadata for the application icon."
                )
                return

            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(
                current_dir,
                "..",
                "assets",
                "neui.png",
            )

            if not os.path.exists(icon_path):
                return

            original_image = skia.Image.MakeFromEncoded(
                skia.Data.MakeFromFileName(icon_path)
            )

            if not original_image:
                self._debug_log("Could not load application icon.")
                return

            icon_images = []

            for size in (16, 32, 48):
                surface = skia.Surface.MakeRasterN32Premul(size, size)
                if surface is None:
                    continue

                canvas = surface.getCanvas()
                canvas.drawImageRect(
                    original_image,
                    skia.Rect.MakeWH(
                        original_image.width(),
                        original_image.height(),
                    ),
                    skia.Rect.MakeWH(size, size),
                    skia.SamplingOptions(skia.FilterMode.kLinear),
                )

                image = surface.makeImageSnapshot()
                bitmap = skia.Bitmap()
                bitmap.allocPixels(
                    skia.ImageInfo.Make(
                        size,
                        size,
                        skia.kRGBA_8888_ColorType,
                        skia.kUnpremul_AlphaType,
                    )
                )

                if not image.readPixels(
                    bitmap.info(),
                    bitmap.getPixels(),
                    bitmap.rowBytes(),
                    0,
                    0,
                ):
                    continue

                flat_pixels = bitmap.tobytes()
                formatted_pixels = []

                for y in range(size):
                    row = []
                    for x in range(size):
                        index = (y * size + x) * 4
                        row.append([
                            flat_pixels[index],
                            flat_pixels[index + 1],
                            flat_pixels[index + 2],
                            flat_pixels[index + 3],
                        ])
                    formatted_pixels.append(row)

                icon_images.append((size, size, formatted_pixels))

            if icon_images:
                glfw.set_window_icon(
                    self.window,
                    len(icon_images),
                    icon_images,
                )

        except Exception as error:
            self._debug_log(f"Failed to set window icon: {error}")

    # ---------------------------------------------------------
    # Graphics backend
    # ---------------------------------------------------------

    def _create_linux_gl_interface(self):
        """Choose the Skia GL interface for the active GLFW platform/API."""
        platform = glfw.get_platform()
        context_api = glfw.get_window_attrib(
            self.window,
            glfw.CONTEXT_CREATION_API,
        )

        # On Wayland, GLFW's native context API is EGL. The GLFW hint may
        # therefore report GLFW_NATIVE_CONTEXT_API even though the context
        # is backed by EGL. On X11, the native API is GLX.
        if platform == glfw.PLATFORM_WAYLAND:
            if context_api not in (
                glfw.NATIVE_CONTEXT_API,
                glfw.EGL_CONTEXT_API,
            ):
                raise RuntimeError(
                    "Unsupported GLFW context creation API on Wayland: "
                    f"{context_api}"
                )

            self._debug_log("Using EGL for the OpenGL context (Wayland).")
            return skia.GrGLInterface.MakeEGL()

        if platform == glfw.PLATFORM_X11:
            if context_api == glfw.EGL_CONTEXT_API:
                self._debug_log("Using EGL for the OpenGL context (X11).")
                return skia.GrGLInterface.MakeEGL()

            if context_api == glfw.NATIVE_CONTEXT_API:
                self._debug_log("Using GLX for the OpenGL context (X11).")
                return skia.GrGLInterface.MakeGLX()

            raise RuntimeError(
                "Unsupported GLFW context creation API on X11: "
                f"{context_api}"
            )

        raise RuntimeError(
            "Unsupported GLFW window platform for Linux OpenGL: "
            f"{platform}"
        )

    def _configure_graphics_backend(self):
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)

        self._print_opengl_info()
        self.stencil_bits = self._query_stencil_bits()

        if sys.platform.startswith("linux"):
            gl_interface = self._create_linux_gl_interface()

            if gl_interface is None:
                raise RuntimeError(
                    "Could not create the Skia OpenGL interface"
                )

            if not gl_interface.validate():
                raise RuntimeError(
                    "Skia OpenGL interface validation failed"
                )

            self.context = skia.GrDirectContext.MakeGL(gl_interface)
        else:
            self.context = skia.GrDirectContext.MakeGL()

        if self.context is None:
            raise RuntimeError(
                "Could not initialize the Skia OpenGL context"
            )

        self.renderer = Renderer()
        self.event_manager = EventManager(self.window)

        self._debug_log("Graphics backend initialized.")

    def _configure_native_window(self):
        if sys.platform == "win32":
            self._configure_windows_titlebar()

        self._configure_window_icon()
        self._configure_graphics_backend()

        glfw.set_window_size_callback(
            self.window,
            self._on_window_resize,
        )
        glfw.set_framebuffer_size_callback(
            self.window,
            self._on_framebuffer_resize,
        )

        window_width, window_height = glfw.get_window_size(self.window)
        fb_width, fb_height = glfw.get_framebuffer_size(self.window)

        self._on_window_resize(
            self.window,
            window_width,
            window_height,
        )
        self._on_framebuffer_resize(
            self.window,
            fb_width,
            fb_height,
        )

    # ---------------------------------------------------------
    # Window callbacks
    # ---------------------------------------------------------

    def _on_window_resize(self, window, width, height):
        if self.root:
            self.root.style["w"] = width
            self.root.style["h"] = height

    def _on_framebuffer_resize(self, window, width, height):
        if width <= 0 or height <= 0:
            self.surface = None
            self.canvas = None
            return

        backend_render_target = skia.GrBackendRenderTarget(
            width,
            height,
            0,
            self.stencil_bits,
            skia.GrGLFramebufferInfo(0, 0x8058),
        )

        self.surface = skia.Surface.MakeFromBackendRenderTarget(
            self.context,
            backend_render_target,
            skia.kBottomLeft_GrSurfaceOrigin,
            skia.kRGBA_8888_ColorType,
            skia.ColorSpace.MakeSRGB(),
        )

        if self.surface is None:
            raise RuntimeError(
                "Failed to create the Skia framebuffer surface"
            )

        self._debug_log(
            "Skia GPU-backed: "
            f"{self.surface.recordingContext() is not None}"
        )
        self.canvas = self.surface.getCanvas()

    # ---------------------------------------------------------
    # UI tree management
    # ---------------------------------------------------------

    def add(self, element):
        self.root = element
        width, height = glfw.get_window_size(self.window)
        self.root.style["w"] = width
        self.root.style["h"] = height

    def add_overlay(self, element):
        self.overlays.append(element)

    def remove_overlay(self, element):
        if element in self.overlays:
            self.overlays.remove(element)

    # ---------------------------------------------------------
    # Resource cleanup
    # ---------------------------------------------------------

    def _cleanup(self):
        """Release Skia references and GLFW resources; safe to call repeatedly."""
        self.canvas = None
        self.surface = None
        self.renderer = None
        self.event_manager = None
        self.context = None

        window = self.window
        self.window = None

        try:
            if window is not None:
                glfw.destroy_window(window)
        except Exception as error:
            self._debug_log(f"Failed to destroy GLFW window: {error}")
        finally:
            if self._glfw_initialized:
                self._glfw_initialized = False
                glfw.terminate()

            if App._instance is self:
                App._instance = None

    # ---------------------------------------------------------
    # Main loop
    # ---------------------------------------------------------

    def run(self):
        if self.window is None:
            raise RuntimeError("Cannot run NEUI App: the window is not initialized")

        self._debug_log("Main loop started.")
        frame_count = 0

        try:
            while not glfw.window_should_close(self.window):
                frame_count += 1
                glfw.poll_events()

                self.event_manager.process_events(
                    self.root,
                    self.overlays,
                )
                animation_manager.update()

                width, height = glfw.get_window_size(self.window)

                if self.root:
                    self.root.computed_bounds = {
                        "x": 0,
                        "y": 0,
                        "w": width,
                        "h": height,
                    }
                    compute_layout(self.root, width, height)

                for overlay in self.overlays:
                    overlay.computed_bounds = {
                        "x": 0,
                        "y": 0,
                        "w": width,
                        "h": height,
                    }
                    compute_layout(overlay, width, height)

                fb_width, fb_height = glfw.get_framebuffer_size(
                    self.window
                )

                if (
                    self.surface is not None
                    and self.canvas is not None
                    and width > 0
                    and height > 0
                    and fb_width > 0
                    and fb_height > 0
                ):
                    self.canvas.clear(skia.Color(30, 30, 30))

                    scale_x = fb_width / width
                    scale_y = fb_height / height

                    self.canvas.save()
                    try:
                        self.canvas.scale(scale_x, scale_y)

                        if self.root:
                            self.root.render(
                                self.canvas,
                                self.renderer,
                            )

                        for overlay in self.overlays:
                            overlay.render(
                                self.canvas,
                                self.renderer,
                            )
                    finally:
                        self.canvas.restore()

                    self.surface.flushAndSubmit()

                glfw.swap_buffers(self.window)

        finally:
            self._debug_log(
                f"Main loop finished. Frames: {frame_count}"
            )
            self._cleanup()

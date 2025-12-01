import glfw
import skia
from .renderer import Renderer
from .events import EventManager
from .layout import compute_layout

class App:
    def __init__(self, title="NEUI App", width=800, height=600, theme="dark"):
        if not glfw.init():
            raise RuntimeError("Could not initialize GLFW")

        # Set window hints for Skia
        glfw.window_hint(glfw.STENCIL_BITS, 8)  # Skia requires a stencil buffer
        glfw.window_hint(glfw.SRGB_CAPABLE, glfw.TRUE)
        
        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Could not create GLFW window")

        glfw.make_context_current(self.window)
        
        # Initialize Skia GPU context (OpenGL)
        self.context = skia.GrDirectContext.MakeGL()
        self.surface = None
        self.canvas = None
        
        self.root = None
        self.renderer = Renderer()
        self.event_manager = EventManager(self.window)
        
        # Setup callbacks
        glfw.set_window_size_callback(self.window, self._on_resize)
        
        # Initial resize to setup surface
        self._on_resize(self.window, width, height)

    def _on_resize(self, window, width, height):
        # Create a new surface matching the window size
        backend_render_target = skia.GrBackendRenderTarget(
            width,
            height,
            0,  # sampleCnt
            0,  # stencilBits (0 means let Skia handle it or match window)
            skia.GrGLFramebufferInfo(0, 0x8058)  # 0x8058 = GL_RGBA8
        )
        
        self.surface = skia.Surface.MakeFromBackendRenderTarget(
            self.context,
            backend_render_target,
            skia.kBottomLeft_GrSurfaceOrigin,
            skia.kRGBA_8888_ColorType,
            skia.ColorSpace.MakeSRGB()
        )
        self.canvas = self.surface.getCanvas()
        
        # Update root size if it exists
        if self.root:
            self.root.style['w'] = width
            self.root.style['h'] = height

    def add(self, element):
        self.root = element
        # Set initial root size to window size
        width, height = glfw.get_window_size(self.window)
        self.root.style['w'] = width
        self.root.style['h'] = height

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            
            # 1. Handle Events (delegated to EventManager)
            self.event_manager.process_events(self.root)
            
            # 2. Layout Pass
            if self.root:
                width, height = glfw.get_window_size(self.window)
                # Ensure root fills window
                self.root.computed_bounds = {'x': 0, 'y': 0, 'w': width, 'h': height}
                compute_layout(self.root, width, height)
            
            # 3. Render Pass
            if self.surface:
                self.canvas.clear(skia.Color(30, 30, 30)) # Default dark bg
                
                if self.root:
                    self.root.render(self.canvas, self.renderer)
                
                self.surface.flushAndSubmit()
                glfw.swap_buffers(self.window)
        
        glfw.terminate()

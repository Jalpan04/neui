import sys
# Prefer the system Fontconfig on Linux.
#
# Load it globally before importing Skia so its symbols can be
# resolved by skia-python instead of its bundled Fontconfig.
# If the system library is unavailable, Skia uses its bundled version.
_fontconfig_handle = None

if sys.platform.startswith("linux"):
    try:
        import ctypes

        _fontconfig_handle = ctypes.CDLL(
            "libfontconfig.so.1",
            mode=ctypes.RTLD_GLOBAL,
        )

    except OSError:
        # Fall back to the Fontconfig bundled with skia-python.
        pass

# Context stack for 'with' statement support
_context_stack = []

from .core.app import App
from . import ui
from . import cui

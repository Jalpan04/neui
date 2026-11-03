import sys
import skia


class FontManager:
    def __init__(self):
        self._manager = skia.FontMgr.RefDefault()
        self._normal_style = skia.FontStyle()

        # Cache installed font families.
        self._families = {family.casefold(): family for family in self._manager}

        self.regular, self.regular_family = self._resolve(default_fonts())

        self.monospace, self.monospace_family = self._resolve(default_monospace_fonts())

    def _resolve(self, families):
        for requested in families:
            actual = self._families.get(requested.casefold())

            if actual is None:
                continue

            typeface = self._manager.matchFamilyStyle(actual, self._normal_style)

            if typeface is not None:
                return typeface, actual

        return skia.Typeface.MakeDefault(), None


def default_fonts() -> tuple[str, ...]:
    """Preferred sans-serif font families for each platform."""

    common = (
        "Noto Sans",
        "DejaVu Sans",
        "Arial",
    )

    if sys.platform == "win32":
        return (
            "Segoe UI",
            *common,
        )

    if sys.platform == "darwin":
        return (
            ".AppleSystemUIFont",
            "Helvetica Neue",
            *common,
        )

    if sys.platform.startswith("linux"):
        return (
            "Noto Sans",
            "Ubuntu",
            "Adwaita Sans",
            "DejaVu Sans",
            "Liberation Sans",
            *common,
        )

    return common


def default_monospace_fonts() -> tuple[str, ...]:
    """Preferred monospace font families for each platform."""

    common = (
        "Noto Sans Mono",
        "DejaVu Sans Mono",
        "Courier New",
    )

    if sys.platform == "win32":
        return (
            "Cascadia Mono",
            "Consolas",
            *common,
        )

    if sys.platform == "darwin":
        return (
            "Menlo",
            "SF Mono",
            *common,
        )

    if sys.platform.startswith("linux"):
        return (
            "Ubuntu Mono",
            "Adwaita Mono",
            *common,
        )

    return common

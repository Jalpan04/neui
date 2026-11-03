from .element import Element


class Text(Element):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self._wrapped_lines = None
        self._wrap_cache_key = None

    def _wrap_text(self, text, max_width, renderer):
        """Wrap text while preserving explicit newline boundaries."""
        text = str(text).replace("\r\n", "\n").replace("\r", "\n")
        wrap_mode = self.style.get("wrap", "word")

        if wrap_mode == "none" or max_width <= 0:
            return text.split("\n")

        lines = []

        # Treat each explicit paragraph independently. split() preserves
        # empty paragraphs, including a trailing newline.
        for paragraph in text.split("\n"):
            if not paragraph:
                lines.append("")
                continue

            if wrap_mode == "word":
                # Keep the existing space-separated wrapping behavior while
                # handling each explicit paragraph independently.
                if paragraph.isspace():
                    lines.append(paragraph)
                    continue

                items = paragraph.split(" ")
                current_line = ""

                for item in items:
                    separator = " " if current_line else ""
                    test_line = current_line + separator + item
                    width, _ = renderer.measure_text(test_line, self.style)

                    if width <= max_width:
                        current_line = test_line
                    elif current_line:
                        lines.append(current_line)
                        current_line = item
                    else:
                        # Keep an overlong word intact on its own line rather
                        # than splitting it unexpectedly.
                        lines.append(item)
                        current_line = ""

                if current_line:
                    lines.append(current_line)

            else:
                # Character wrapping is useful for long unbroken strings.
                current_line = ""

                for character in paragraph:
                    test_line = current_line + character
                    width, _ = renderer.measure_text(test_line, self.style)

                    if current_line and width > max_width:
                        lines.append(current_line)
                        current_line = character
                    else:
                        current_line = test_line

                if current_line:
                    lines.append(current_line)

        # An empty input still occupies one text line.
        return lines if lines else [""]

    def _get_wrapped_lines(self, text, max_width, renderer):
        """Return cached lines while the wrapping inputs remain unchanged."""
        text = str(text)
        cache_key = (
            text,
            max_width,
            self.style.get("wrap", "word"),
            self.style.get("font_size", 14),
            id(renderer),
        )

        if cache_key != self._wrap_cache_key:
            self._wrapped_lines = self._wrap_text(
                text,
                max_width,
                renderer,
            )
            self._wrap_cache_key = cache_key

        return self._wrapped_lines

    def render(self, canvas, renderer):
        bounds = self.computed_bounds
        wrap_mode = self.style.get("wrap", "none")
        max_width = bounds.get("w", 0)

        if wrap_mode != "none" and max_width > 0:
            lines = self._get_wrapped_lines(
                self.text,
                max_width,
                renderer,
            )

            font_size = self.style.get("font_size", 14)
            line_height = self.style.get(
                "line_height",
                font_size * 1.2,
            )

            for index, line in enumerate(lines):
                line_y = bounds["y"] + index * line_height
                renderer.draw_text(
                    canvas,
                    line,
                    bounds["x"],
                    line_y,
                    self.style,
                )
        else:
            # Renderer.draw_text handles explicit newline characters.
            renderer.draw_text(
                canvas,
                self.text,
                bounds["x"],
                bounds["y"],
                self.style,
            )

    def measure(self, parent_w, parent_h):
        from neui import App

        app = App.get_instance()

        if app is None or not hasattr(app, "renderer") or app.renderer is None:
            raise RuntimeError(
                "Text.measure() requires an initialized App renderer"
            )

        renderer = app.renderer
        wrap_mode = self.style.get("wrap", "none")
        max_width = self.style.get(
            "max_width",
            parent_w if parent_w else 0,
        )

        if wrap_mode != "none" and max_width > 0:
            lines = self._get_wrapped_lines(
                self.text,
                max_width,
                renderer,
            )

            font_size = self.style.get("font_size", 14)
            line_height = self.style.get(
                "line_height",
                font_size * 1.2,
            )

            # Use the renderer's actual font metrics for the first line,
            # then add the configured spacing for each additional line.
            _, first_line_height = renderer.measure_text("Ay", self.style)
            total_height = first_line_height + (len(lines) - 1) * line_height

            return max_width, total_height

        return renderer.measure_text(self.text, self.style)

# NEUI (Neo UI)

**NEUI** is a modern, GPU-accelerated Python UI framework featuring a Flexbox-like layout engine, reactive event system, and beautiful default styling. Build desktop applications with the simplicity of web frameworks.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

- **🎨 Modern Look**: Dark mode by default, rounded corners, smooth GPU-accelerated rendering
- **📐 Flexbox Layout**: Intuitive `row` and `col` layouts with `justify`, `align`, and `gap` properties
- **⚡ GPU Accelerated**: Built on `skia-python` and `glfw` for high-performance rendering
- **🖱️ Interactive**: Full event system with Hover, Click, Focus, Blur, and Keyboard events
- **🧩 Rich Components**: Pre-built UI and interactive components ready to use
- **🐍 Pythonic API**: Context managers (`with` statements) for clean, nested layouts
- **🎯 Zero Boilerplate**: Minimal setup, maximum productivity

## 📦 Installation

```bash
pip install neui
```

## 🚀 Quick Start: Registration Form

```python
from neui import App, ui, cui

class FormApp:
    def __init__(self):
        self.name_input = None
        self.email_input = None
        self.result_text = None

    def on_submit(self):
        name = self.name_input.text if self.name_input else "N/A"
        email = self.email_input.text if self.email_input else "N/A"
        
        if self.result_text:
            self.result_text.text = f"Name: {name}\\nEmail: {email}"
            print(f"Form submitted: {name}, {email}")

    def build(self):
        app = App(title="NEUI Form Example", width=600, height=400)
        
        with ui.Box(style={
            "bg": "#0D1117",
            "w": "100%",
            "h": "100%",
            "padding": 30,
            "layout": "col",
            "gap": 20
        }) as root:
            
            # Header
            ui.Text("User Registration", style={
                "font_size": 32,
                "color": "#58A6FF",
                "weight": "bold"
            })
            
            # Form Card
            with cui.Card(style={
                "w": "100%",
                "bg": "#161B22",
                "padding": 25,
                "radius": 8,
                "layout": "col",
                "gap": 15
            }):
                ui.Text("Name", style={"font_size": 14, "color": "#C9D1D9"})
                self.name_input = ui.Input(
                    placeholder="Enter your name",
                    style={"w": "100%", "bg": "#0D1117", "radius": 6}
                )
                
                ui.Text("Email", style={"font_size": 14, "color": "#C9D1D9"})
                self.email_input = ui.Input(
                    placeholder="your.email@example.com",
                    style={"w": "100%", "bg": "#0D1117", "radius": 6}
                )
            
            # Submit Button
            cui.Button(
                "Submit",
                on_click=self.on_submit,
                style={"w": 120, "h": 40, "bg": "#238636", "radius": 6}
            )
            
            # Result Display
            with cui.Card(style={"w": "100%", "bg": "#161B22", "padding": 20}):
                ui.Text("Form Data:", style={"font_size": 16, "color": "#58A6FF"})
                self.result_text = ui.Text(
                    "Fill out the form and click Submit",
                    style={"font_size": 12, "color": "#8B949E"}
                )

        app.add(root)
        app.run()

if __name__ == "__main__":
    form = FormApp()
    form.build()
```

## 📚 Component Library

### UI Components (`neui.ui`)
Basic building blocks for your interface:

| Component | Description |
|-----------|-------------|
| `Box` | Container for layout with flexbox-like properties |
| `Text` | Render text with custom styling |
| `Input` | Text input field with placeholder and password mode |
| `Image` | Display images |
| `ScrollView` | Scrollable container for overflow content |

### Interactive Components (`neui.cui`)
Pre-styled, ready-to-use interactive widgets:

| Component | Description |
|-----------|-------------|
| `Button` | Clickable button with hover/press states |
| `Card` | Container with built-in elevation and styling |
| `Checkbox` | Toggle checkbox with label |
| `Radio` | Radio button with group support |
| `Slider` | Range slider for numeric input |
| `Toggle` | Switch-style boolean input |
| `ProgressBar` | Visual progress indicator |
| `Drawer` | Slide-out panel for navigation |
| `ToastManager` | Notification system |

## 🎨 Styling System

NEUI uses a simple dictionary-based styling system:

```python
style = {
    # Layout
    "layout": "row",      # or "col"
    "gap": 10,            # spacing between children
    "padding": 20,        # internal spacing
    "align": "center",    # vertical alignment
    "justify": "start",   # horizontal alignment
    
    # Dimensions
    "w": 200,             # width (px or "100%")
    "h": 50,              # height
    
    # Appearance
    "bg": "#0D1117",      # background color (hex)
    "color": "white",     # text color
    "radius": 8,          # border radius
    "border_color": "#333",
    "border_width": 1,
    
    # Typography
    "font_size": 14,
    "weight": "bold",
}
```

## 🏗️ Layout Examples

### Row Layout (Horizontal)
```python
with ui.Box(style={"layout": "row", "gap": 10}):
    cui.Button("Button 1")
    cui.Button("Button 2")
    cui.Button("Button 3")
```

### Column Layout (Vertical)
```python
with ui.Box(style={"layout": "col", "gap": 15}):
    ui.Text("Item 1")
    ui.Text("Item 2")
    ui.Text("Item 3")
```

### Nested Layouts
```python
with ui.Box(style={"layout": "col", "gap": 20}):
    ui.Text("Header", style={"font_size": 24})
    
    with ui.Box(style={"layout": "row", "gap": 10}):
        cui.Button("Left")
        cui.Button("Right")
    
    ui.Text("Footer")
```

## 🎯 Examples

Check out the `examples/` directory for complete working examples:

- **form_example.py** - Comprehensive registration form with all input types
- More examples coming soon!

## 📖 Documentation

For detailed documentation including API reference and advanced usage, see [DOCUMENTATION.md](DOCUMENTATION.md).

## 🛠️ Development

```bash
# Clone the repository
git clone https://github.com/Jalpan04/neui.git
cd neui

# Install in editable mode
pip install -e .

# Run examples
python examples/form_example.py
```

## 🐛 Known Limitations

- Currently Windows-only (macOS and Linux support planned)
- No built-in text wrapping (manual line breaks required)
- Limited to OpenGL-compatible systems

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 👤 Author

**Jalpan Vyas**  
Email: vyasjalpan1202@gmail.com  
GitHub: [@Jalpan04](https://github.com/Jalpan04)

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

Built with ❤️ using Python, Skia, and GLFW

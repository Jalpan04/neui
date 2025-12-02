# NEUI Documentation

Complete API reference and usage guide for NEUI - the modern, GPU-accelerated Python UI framework.

## Table of Contents

- [Getting Started](#getting-started)
- [Core Concepts](#core-concepts)
- [UI Components](#ui-components)
- [Interactive Components](#interactive-components)
- [Styling System](#styling-system)
- [Event Handling](#event-handling)
- [Layout System](#layout-system)
- [Examples](#examples)

---

## Getting Started

### Installation

```bash
pip install neui
```

### Your First App

```python
from neui import App, ui

app = App(title="My First NEUI App", width=400, height=300)

with ui.Box(style={"bg": "#0D1117", "w": "100%", "h": "100%", "padding": 20}) as root:
    ui.Text("Hello, NEUI!", style={"font_size": 24, "color": "white"})

app.add(root)
app.run()
```

---

## Core Concepts

### The App Class

Every NEUI application starts with an `App` instance:

```python
from neui import App

app = App(
    title="Window Title",    # Window title bar text
    width=800,              # Window width in pixels
    height=600,             # Window height in pixels
    theme="dark"           # Theme (currently only "dark" supported)
)
```

### Context Managers

NEUI uses Python's `with` statement for clean, nested UI structures:

```python
with ui.Box() as container:
    ui.Text("Child 1")
    ui.Text("Child 2")
    
    with ui.Box() as nested:
        ui.Text("Nested child")
```

This automatically adds children to their parent containers.

### The Style Dictionary

All components accept a `style` parameter:

```python
ui.Text("Styled text", style={
    "font_size": 16,
    "color": "#58A6FF",
    "weight": "bold"
})
```

---

## UI Components

### Box

The fundamental container for laying out other elements.

**Import**: `from neui import ui`

**Parameters**:
- `style` (dict): Styling properties

**Example**:
```python
with ui.Box(style={
    "layout": "col",      # vertical layout
    "gap": 10,            # 10px spacing between children
    "padding": 20,        # 20px internal padding
    "bg": "#1E1E1E",     # background color
    "radius": 8          # rounded corners
}):
    ui.Text("Item 1")
    ui.Text("Item 2")
```

**Common Style Properties**:
- `layout`: `"row"` (horizontal) or `"col"` (vertical)
- `gap`: Spacing between children (pixels)
- `padding`: Internal spacing (pixels)
- `align`: Cross-axis alignment (`"start"`, `"center"`, `"end"`)
- `justify`: Main-axis alignment (`"start"`, `"center"`, `"end"`)
- `w`, `h`: Width and height (pixels or `"100%"`)
- `bg`: Background color (hex string)
- `radius`: Border radius (pixels)

---

### Text

Display text with custom styling.

**Import**: `from neui import ui`

**Parameters**:
- `text` (str): The text to display
- `style` (dict): Styling properties

**Example**:
```python
ui.Text("Hello World", style={
    "font_size": 24,
    "color": "#58A6FF",
    "weight": "bold"
})
```

**Style Properties**:
- `font_size`: Font size in pixels (default: 14)
- `color`: Text color (hex string or color name)
- `weight`: Font weight (`"normal"` or `"bold"`)

---

### Input

Text input field with placeholder and password mode support.

**Import**: `from neui import ui`

**Parameters**:
- `placeholder` (str): Placeholder text
- `password` (bool): If True, masks input characters
- `style` (dict): Styling properties

**Example**:
```python
# Regular text input
name_input = ui.Input(
    placeholder="Enter your name",
    style={
        "w": 300,
        "padding": 12,
        "bg": "#2D333B",
        "radius": 6,
        "color": "white"
    }
)

# Password input
password_input = ui.Input(
    placeholder="Enter password",
    password=True,
    style={"w": 300}
)
```

**Properties**:
- `text`: Get/set the current text value
- `cursor_pos`: Current cursor position
- `focused`: Whether the input has focus

**Events**:
- `on_focus()`: Called when input gains focus
- `on_blur()`: Called when input loses focus
- `on_char(codepoint)`: Called for each character typed
- `on_keydown(key, mods)`: Called for special keys (Backspace, arrows, etc.)

**Example - Reading Input Value**:
```python
username = ui.Input(placeholder="Username")

def on_submit():
    print(f"Username: {username.text}")

cui.Button("Submit", on_click=on_submit)
```

---

### Image

Display images from file paths.

**Import**: `from neui import ui`

**Parameters**:
- `path` (str): Path to image file
- `style` (dict): Styling properties

**Example**:
```python
ui.Image("path/to/image.png", style={
    "w": 200,
    "h": 150
})
```

---

### ScrollView

Scrollable container for content that overflows.

**Import**: `from neui import ui`

**Parameters**:
- `style` (dict): Styling properties

**Example**:
```python
with ui.ScrollView(style={"w": 300, "h": 400, "bg": "#1E1E1E"}):
    for i in range(50):
        ui.Text(f"Item {i}")
```

---

## Interactive Components

### Button

Clickable button with hover and press states.

**Import**: `from neui import cui`

**Parameters**:
- `text` (str): Button label
- `on_click` (callable): Function to call when clicked
- `style` (dict): Styling properties

**Example**:
```python
def handle_click():
    print("Button clicked!")

cui.Button(
    "Click Me",
    on_click=handle_click,
    style={
        "w": 120,
        "h": 40,
        "bg": "#238636",      # green background
        "radius": 6,
        "font_size": 14
    }
)
```

**Default Colors**:
- Normal: `#007ACC` (blue)
- Hover: Lighter blue
- Pressed: Darker blue

**Events**:
- `on_click()`: Called when button is clicked
- `on_mouse_enter()`: Called when mouse hovers over
- `on_mouse_leave()`: Called when mouse leaves
- `on_mouse_down(x, y)`: Called when mouse button pressed
- `on_mouse_up()`: Called when mouse button released

---

### Card

Styled container with built-in elevation and rounded corners.

**Import**: `from neui import cui`

**Parameters**:
- `style` (dict): Styling properties

**Example**:
```python
with cui.Card(style={
    "w": "100%",
    "padding": 20,
    "bg": "#161B22",
    "radius": 8
}):
    ui.Text("Card Title", style={"font_size": 18, "color": "white"})
    ui.Text("Card content goes here", style={"color": "#8B949E"})
```

**Default Style**:
- Rounded corners
- Subtle shadow
- Dark background

---

### Checkbox

Toggle checkbox for boolean input.

**Import**: `from neui import cui`

**Parameters**:
- `checked` (bool): Initial checked state
- `style` (dict): Styling properties

**Example**:
```python
newsletter_checkbox = cui.Checkbox(
    checked=False,
    style={"w": 20, "h": 20}
)

# Read state
if newsletter_checkbox.checked:
    print("Subscribed to newsletter")
```

**Properties**:
- `checked`: Get/set the checked state (bool)

**Events**:
- `on_click()`: Toggles checked state

---

### Radio

Radio button for mutually exclusive selections.

**Import**: `from neui import cui`

**Parameters**:
- `group` (str): Group name (only one radio per group can be selected)
- `checked` (bool): Initial checked state
- `style` (dict): Styling properties

**Example**:
```python
male_radio = cui.Radio(group="gender", checked=True)
female_radio = cui.Radio(group="gender", checked=False)
other_radio = cui.Radio(group="gender", checked=False)

# Read selected value
if male_radio.checked:
    print("Male selected")
elif female_radio.checked:
    print("Female selected")
elif other_radio.checked:
    print("Other selected")
```

**Properties**:
- `checked`: Whether this radio is selected
- `group`: Group name

---

### Slider

Range slider for numeric input.

**Import**: `from neui import cui`

**Parameters**:
- `min_val` (float): Minimum value
- `max_val` (float): Maximum value
- `value` (float): Initial value
- `style` (dict): Styling properties

**Example**:
```python
age_slider = cui.Slider(
    min_val=18,
    max_val=100,
    value=25,
    style={"w": 300}
)

# Read value
print(f"Age: {int(age_slider.value)}")
```

**Properties**:
- `value`: Current slider value (float)
- `min_val`: Minimum value
- `max_val`: Maximum value

---

### Toggle

Switch-style boolean input.

**Import**: `from neui import cui`

**Parameters**:
- `value` (bool): Initial state
- `style` (dict): Styling properties

**Example**:
```python
dark_mode_toggle = cui.Toggle(
    value=True,
    style={"w": 50, "h": 25}
)

# Read state
if dark_mode_toggle.value:
    print("Dark mode enabled")
```

**Properties**:
- `value`: Get/set the toggle state (bool)

---

### ProgressBar

Visual progress indicator.

**Import**: `from neui import cui`

**Parameters**:
- `value` (float): Progress value (0.0 to 1.0)
- `style` (dict): Styling properties

**Example**:
```python
progress = cui.ProgressBar(
    value=0.5,  # 50% complete
    style={"w": 300, "h": 20}
)

# Update progress
progress.value = 0.75  # 75% complete
```

**Properties**:
- `value`: Progress from 0.0 (0%) to 1.0 (100%)

---

### Drawer

Slide-out panel for navigation or settings.

**Import**: `from neui import cui`

**Parameters**:
- `side` (str): Which side to slide from (`"left"`, `"right"`, `"top"`, `"bottom"`)
- `style` (dict): Styling properties

**Example**:
```python
drawer = cui.Drawer(
    side="left",
    style={"w": 250, "bg": "#161B22"}
)

with drawer:
    ui.Text("Menu Item 1")
    ui.Text("Menu Item 2")

# Show/hide drawer
drawer.open()
drawer.close()
```

---

### ToastManager

Notification system for temporary messages.

**Import**: `from neui import cui`

**Example**:
```python
toast_manager = cui.ToastManager()

# Show notification
toast_manager.show("Operation successful!", duration=3.0)
toast_manager.show("Error occurred!", duration=5.0, type="error")
```

---

## Styling System

### Color Formats

NEUI supports multiple color formats:

```python
# Hex colors
"#FF0000"        # Red
"#00FF00"        # Green
"#0000FFAA"      # Blue with alpha

# Named colors
"white"
"black"
"red"
"green"
"blue"
```

### Dimension Units

Dimensions can be specified as:

```python
"w": 200         # Pixels
"w": "100%"      # Percentage of parent
"w": "50%"       # Half of parent
```

### Complete Style Reference

```python
style = {
    # Layout
    "layout": "row" | "col",
    "gap": <pixels>,
    "padding": <pixels>,
    "align": "start" | "center" | "end",
    "justify": "start" | "center" | "end",
    
    # Dimensions
    "w": <pixels> | "<percentage>%",
    "h": <pixels> | "<percentage>%",
    
    # Appearance
    "bg": <color>,
    "color": <color>,
    "radius": <pixels>,
    "border_color": <color>,
    "border_width": <pixels>,
    "shadow": <blur_pixels>,
    
    # Typography
    "font_size": <pixels>,
    "weight": "normal" | "bold",
}
```

---

## Event Handling

### Available Events

All interactive components support these events:

- **Mouse Events**:
  - `on_click()`: Mouse click
  - `on_mouse_enter()`: Mouse enters element
  - `on_mouse_leave()`: Mouse leaves element
  - `on_mouse_down(x, y)`: Mouse button pressed
  - `on_mouse_up()`: Mouse button released
  - `on_mouse_move(x, y)`: Mouse moves over element

- **Focus Events**:
  - `on_focus()`: Element gains focus
  - `on_blur()`: Element loses focus

- **Keyboard Events** (for focused elements):
  - `on_keydown(key, mods)`: Key pressed
  - `on_keyup(key, mods)`: Key released
  - `on_char(codepoint)`: Character input

### Event Example

```python
from neui import ui, cui
import glfw

class MyApp:
    def __init__(self):
        self.input_field = None
    
    def build(self):
        self.input_field = ui.Input(placeholder="Type here...")
        
        # Override keyboard event
        original_keydown = self.input_field.on_keydown
        def custom_keydown(key, mods):
            if key == glfw.KEY_ENTER:
                print(f"Submitted: {self.input_field.text}")
            else:
                original_keydown(key, mods)
        
        self.input_field.on_keydown = custom_keydown
```

---

## Layout System

### Flexbox-like Layouts

NEUI uses a layout system inspired by CSS Flexbox:

#### Row Layout (Horizontal)

```python
with ui.Box(style={"layout": "row", "gap": 10}):
    cui.Button("Button 1")
    cui.Button("Button 2")
    cui.Button("Button 3")
```

#### Column Layout (Vertical)

```python
with ui.Box(style={"layout": "col", "gap": 10}):
    ui.Text("Item 1")
    ui.Text("Item 2")
    ui.Text("Item 3")
```

### Alignment

Control how children are positioned:

```python
# Center horizontally
with ui.Box(style={"layout": "row", "justify": "center"}):
    cui.Button("Centered")

# Center vertically
with ui.Box(style={"layout": "col", "align": "center"}):
    ui.Text("Centered")

# Center both axes
with ui.Box(style={"justify": "center", "align": "center", "w": "100%", "h": "100%"}):
    ui.Text("Center of screen")
```

### Spacing

```python
with ui.Box(style={
    "gap": 15,      # Space between children
    "padding": 20   # Space inside container
}):
    ui.Text("Item 1")
    ui.Text("Item 2")
```

---

## Examples

### Complete Form Example

See [examples/form_example.py](../examples/form_example.py) for a comprehensive form demonstrating:
- Text, email, and password inputs
- Checkboxes and radio buttons
- Sliders and toggles
- Buttons with event handlers
- Nested layouts
- Card containers

### Minimal Counter App

```python
from neui import App, ui, cui

class CounterApp:
    def __init__(self):
        self.count = 0
        self.label = None
    
    def increment(self):
        self.count += 1
        if self.label:
            self.label.text = f"Count: {self.count}"
    
    def build(self):
        app = App(title="Counter", width=300, height=200)
        
        with ui.Box(style={
            "bg": "#0D1117",
            "w": "100%",
            "h": "100%",
            "layout": "col",
            "justify": "center",
            "align": "center",
            "gap": 20
        }) as root:
            self.label = ui.Text(
                f"Count: {self.count}",
                style={"font_size": 24, "color": "white"}
            )
            
            cui.Button(
                "Increment",
                on_click=self.increment,
                style={"w": 120, "h": 40}
            )
        
        app.add(root)
        app.run()

if __name__ == "__main__":
    counter = CounterApp()
    counter.build()
```

### Grid Layout

```python
with ui.Box(style={"layout": "col", "gap": 10, "padding": 20}):
    # Row 1
    with ui.Box(style={"layout": "row", "gap": 10}):
        cui.Button("1")
        cui.Button("2")
        cui.Button("3")
    
    # Row 2
    with ui.Box(style={"layout": "row", "gap": 10}):
        cui.Button("4")
        cui.Button("5")
        cui.Button("6")
```

---

## Best Practices

### 1. Store Component References

Store references to components you need to update:

```python
self.status_text = ui.Text("Ready")

def update_status(self, message):
    self.status_text.text = message
```

### 2. Use Descriptive Styling

Create style dictionaries for reusability:

```python
CARD_STYLE = {
    "bg": "#161B22",
    "padding": 20,
    "radius": 8
}

with cui.Card(style=CARD_STYLE):
    ui.Text("Content")
```

### 3. Organize with Classes

Encapsulate your UI in a class:

```python
class MyApp:
    def __init__(self):
        # Initialize state
        pass
    
    def build(self):
        # Build UI
        pass
    
    def on_action(self):
        # Handle events
        pass
```

### 4. Use Context Managers

Always use `with` statements for containers:

```python
# Good
with ui.Box():
    ui.Text("Child")

# Avoid
box = ui.Box()
box.add(ui.Text("Child"))
```

---

## Troubleshooting

### Component Not Showing?

- Check that parent container has `"w"` and `"h"` set
- Verify background color isn't same as content color
- Ensure component is added to the root hierarchy

### Layout Issues?

- Check `layout` property is set (`"row"` or `"col"`)
- Verify `gap` and `padding` values
- Use `align` and `justify` for positioning

### Events Not Firing?

- Ensure component has focus (for keyboard events)
- Check that event handler is properly bound
- Verify mouse is hovering over correct element

---

## Advanced Topics

### Animations

```python
# Animate style properties
element.animate(
    properties={"w": 200, "h": 100},
    duration=0.3,
    easing="ease-in-out"
)
```

### Custom Components

Create reusable custom components by subclassing `Box`:

```python
from neui.ui.box import Box

class CustomButton(Box):
    def __init__(self, label, **kwargs):
        super().__init__(**kwargs)
        # Custom initialization
```

---

For more examples and updates, visit the [GitHub repository](https://github.com/Jalpan04/neui).

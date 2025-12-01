import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from neui import App, ui, cui

class CalculatorApp:
    def __init__(self):
        self.display_text = "0"
        self.display_element = None
        self.current_op = None
        self.prev_val = 0
        self.new_entry = True

    def on_digit(self, digit):
        if self.new_entry:
            self.display_text = str(digit)
            self.new_entry = False
        else:
            self.display_text += str(digit)
        self.update_display()

    def on_op(self, op):
        self.prev_val = float(self.display_text)
        self.current_op = op
        self.new_entry = True

    def on_equal(self):
        if self.current_op:
            curr = float(self.display_text)
            if self.current_op == '+': res = self.prev_val + curr
            elif self.current_op == '-': res = self.prev_val - curr
            elif self.current_op == '*': res = self.prev_val * curr
            elif self.current_op == '/': res = self.prev_val / curr if curr != 0 else 0
            
            # Format result
            if res.is_integer():
                self.display_text = str(int(res))
            else:
                self.display_text = str(res)
            
            self.current_op = None
            self.new_entry = True
            self.update_display()

    def on_clear(self):
        self.display_text = "0"
        self.current_op = None
        self.prev_val = 0
        self.new_entry = True
        self.update_display()

    def update_display(self):
        if self.display_element:
            self.display_element.text = self.display_text
            # Simple font scaling
            length = len(self.display_text)
            if length > 10:
                self.display_element.style['font_size'] = max(20, 40 - (length - 10) * 2)
            else:
                self.display_element.style['font_size'] = 40

    def build(self):
        app = App(title="NEUI Calculator", width=360, height=550)
        
        with ui.Box(style={"bg": "#121212", "w": "100%", "h": "100%", "padding": 20, "layout": "col", "gap": 15}) as root:
            
            # Display
            with cui.Card(style={"w": "100%", "h": 100, "bg": "#1E1E1E", "justify": "end", "align": "end", "padding": 20}):
                self.display_element = ui.Text("0", style={"font_size": 40, "color": "white", "weight": "bold"})

            # Keypad
            rows = [
                ['7', '8', '9', '/'],
                ['4', '5', '6', '*'],
                ['1', '2', '3', '-'],
                ['C', '0', '=', '+']
            ]
            
            # Calculate button size
            # Width 360 - 40 padding = 320.
            # 3 gaps of 10 = 30.
            # Remaining = 290. / 4 = 72.5.
            # Let's use 70px buttons.
            
            for row in rows:
                with ui.Box(style={"layout": "row", "gap": 12, "w": "100%", "h": 70}):
                    for key in row:
                        color = "#333333"
                        if key in ['/', '*', '-', '+', '=']: color = "#FF9F0A"
                        if key == 'C': color = "#A5A5A5"
                        
                        # Capture key in closure
                        def make_handler(k):
                            if k.isdigit(): return lambda: self.on_digit(int(k))
                            if k in ['+', '-', '*', '/']: return lambda: self.on_op(k)
                            if k == '=': return self.on_equal
                            if k == 'C': return self.on_clear
                            return None

                        # Circular buttons
                        cui.Button(key, on_click=make_handler(key), 
                                   style={"w": 70, "h": 70, "bg": color, "radius": 35, "font_size": 28})

        app.add(root)
        app.run()

if __name__ == "__main__":
    calc = CalculatorApp()
    calc.build()

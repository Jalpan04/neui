import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from neui import App, ui, cui

def on_login():
    print("Attempting Login...")

def on_signup():
    print("Switching to Signup...")

def on_dark_mode(checked):
    print(f"Dark Mode: {checked}")

def on_volume(value):
    print(f"Volume: {int(value * 100)}%")

def main():
    app = App(title="NEUI Showcase", width=1000, height=700)

    # Main Container
    with ui.Box(style={
        "bg": "#121212",
        "w": "100%", "h": "100%",
        "layout": "row", # Split view
    }) as root:
        
        # Left Sidebar (Navigation)
        with ui.Box(style={
            "w": 250, "h": "100%",
            "bg": "#1E1E1E",
            "padding": 20,
            "layout": "col",
            "gap": 10
        }):
            ui.Text("NEUI", style={"color": "#007ACC", "font_size": 28, "weight": "bold"})
            ui.Text("v0.1.0", style={"color": "#666", "font_size": 12})
            
            # Spacer
            ui.Box(style={"h": 20})
            
            # Nav Items (Simulated Buttons)
            cui.Button("Dashboard", style={"w": "100%", "bg": "#2D2D2D", "justify": "start", "padding": 12})
            cui.Button("Settings", style={"w": "100%", "bg": "#1E1E1E", "justify": "start", "padding": 12})
            cui.Button("Profile", style={"w": "100%", "bg": "#1E1E1E", "justify": "start", "padding": 12})

        # Right Content Area
        with ui.Box(style={
            "w": "100%", "h": "100%", # Flex grow
            "padding": 40,
            "layout": "col",
            "gap": 30
        }):
            # Header
            with ui.Box(style={"layout": "col", "gap": 5}):
                ui.Text("Welcome Back, User", style={"font_size": 32, "weight": "bold"})
                ui.Text("Here is what's happening today.", style={"color": "#888", "font_size": 16})

            # Content Grid (Cards)
            with ui.Box(style={"layout": "row", "gap": 20}):
                
                # Login Card Demo
                with cui.Card(style={"w": 350, "padding": 30, "gap": 15}):
                    ui.Text("Interactive Login", style={"font_size": 20, "weight": "bold"})
                    
                    ui.Input(placeholder="Username", style={"w": "100%"})
                    ui.Input(placeholder="Password", password=True, style={"w": "100%"})
                    
                    with ui.Box(style={"layout": "row", "gap": 10, "justify": "end", "w": "100%"}):
                        cui.Button("Sign Up", on_click=on_signup, style={"bg": "#333", "w": 80})
                        cui.Button("Login", on_click=on_login, style={"w": 80})

                # Settings Card
                with cui.Card(style={"w": 350, "padding": 30, "gap": 20}):
                    ui.Text("Quick Settings", style={"font_size": 20, "weight": "bold"})
                    
                    # Toggle Row
                    with ui.Box(style={"layout": "row", "justify": "space-between", "align": "center", "w": "100%"}):
                        ui.Text("Dark Mode", style={"color": "#DDD"})
                        cui.Toggle(checked=True, on_change=on_dark_mode)
                        
                    # Slider Row
                    with ui.Box(style={"layout": "col", "gap": 10, "w": "100%"}):
                        with ui.Box(style={"layout": "row", "justify": "space-between", "w": "100%"}):
                            ui.Text("Volume", style={"color": "#DDD"})
                            ui.Text("75%", style={"color": "#AAA", "font_size": 12})
                        
                        cui.Slider(value=0.75, on_change=on_volume, style={"w": "100%"})

    app.add(root)
    app.run()

if __name__ == "__main__":
    main()

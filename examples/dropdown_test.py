from neui import App, ui, cui

def build():
    app = App(title="Dropdown Test", width=400, height=400)
    
    with ui.Box(style={'padding': 20, 'gap': 20, 'layout': 'col', 'bg': '#0D1117'}) as root:
        ui.Text("Dropdown Example", style={'font_size': 20, 'color': '#58A6FF'})
        
        # Result Text
        result = ui.Text("Selected: Option 1", style={'color': '#8B949E'})
        
        def on_change(val):
            result.text = f"Selected: {val}"
            print(f"Dropdown changed to: {val}")
            
        # Dropdown 1
        ui.Text("Basic Dropdown:")
        dd = cui.Dropdown(
            options=["Option 1", "Option 2", "Option 3", "Option 4"],
            on_change=on_change,
            style={'w': 200}
        )
        
        # Dropdown 2
        ui.Text("Pre-selected Value:")
        dd2 = cui.Dropdown(
            options=["Red", "Green", "Blue"],
            value="Green",
            style={'w': 150}
        )
        
        # Dropdown 3 (Bottom to test overlay positioning)
        with ui.Box(style={'margin_top': 50}):
             ui.Text("Bottom Dropdown:")
             cui.Dropdown(
                options=["A", "B", "C"],
                style={'w': 100}
            )

    app.add(root)
    app.run()

if __name__ == "__main__":
    build()

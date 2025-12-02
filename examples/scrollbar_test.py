from neui import App, ui, cui

def build():
    app = App(title="Scrollbar Test", width=400, height=500)
    
    with ui.Box(style={'padding': 20, 'layout': 'col', 'gap': 10, 'bg': '#0D1117'}) as root:
        ui.Text("Scrollbar Test", style={'font_size': 20, 'color': '#58A6FF'})
        ui.Text("Try dragging the scrollbar or using mouse wheel.", style={'color': '#8B949E', 'font_size': 14})
        
        # ScrollView with lots of content
        with ui.ScrollView(style={
            'w': 300, 
            'h': 300, 
            'bg': '#161B22', 
            'radius': 8,
            'border_color': '#30363D',
            'border_width': 1,
            'scrollbar_width': 12,
            'scrollbar_color': '#58A6FF40',
            'scrollbar_hover_color': '#58A6FF80'
        }):
            with ui.Box(style={'layout': 'col', 'gap': 10, 'padding': 15}):
                for i in range(20):
                    with cui.Card(style={'w': '100%', 'padding': 10, 'bg': '#21262D'}):
                        ui.Text(f"Item {i+1}", style={'weight': 'bold'})
                        ui.Text(f"This is the content for item {i+1}. It has some text to take up space.", style={'wrap': 'word','color': '#8B949E', 'font_size': 12})
                        
    app.add(root)
    app.run()

if __name__ == "__main__":
    build()

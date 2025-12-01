import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from neui import App, ui, cui

class TodoApp:
    def __init__(self):
        self.items = []
        self.list_container = None
        self.input_element = None

    def add_item(self):
        text = self.input_element.text
        if text:
            self.items.append({"text": text, "done": False})
            self.input_element.text = "" # Clear input
            self.input_element.cursor_pos = 0
            self.render_list()

    def toggle_item(self, index, checked):
        self.items[index]['done'] = checked
        # Visual update handled by toggle state, but we sync data here

    def delete_item(self, index):
        self.items.pop(index)
        self.render_list()

    def render_list(self):
        # Clear current list
        self.list_container.children = []
        
        for i, item in enumerate(self.items):
            # Create Row for item
            row = ui.Box(style={
                "layout": "row", 
                "w": "100%", 
                "h": 50, 
                "bg": "#333", 
                "radius": 8, 
                "padding": 10,
                "align": "center",
                "justify": "space-between",
                "gap": 10
            })
            
            # Checkbox (Toggle)
            # Capture index
            def make_toggle_handler(idx):
                return lambda c: self.toggle_item(idx, c)
            
            t = cui.Toggle(checked=item['done'], on_change=make_toggle_handler(i))
            row.add(t)
            
            # Text
            txt = ui.Text(item['text'], style={"color": "white", "font_size": 16})
            row.add(txt)
            
            # Delete Button
            def make_del_handler(idx):
                return lambda: self.delete_item(idx)
                
            btn = cui.Button("X", on_click=make_del_handler(i), style={"w": 30, "h": 30, "bg": "#FF3B30", "padding": 0})
            row.add(btn)
            
            self.list_container.add(row)

    def build(self):
        app = App(title="NEUI Todo", width=400, height=600)
        
        with ui.Box(style={"bg": "#1E1E1E", "w": "100%", "h": "100%", "padding": 20, "layout": "col", "gap": 20}) as root:
            
            ui.Text("My Tasks", style={"font_size": 28, "weight": "bold", "color": "#007ACC"})
            
            # Input Area
            with ui.Box(style={"layout": "row", "gap": 10, "w": "100%", "h": 40}):
                self.input_element = ui.Input(placeholder="Add a new task...", style={"w": "100%", "bg": "#333"})
                cui.Button("Add", on_click=self.add_item, style={"w": 80, "bg": "#007ACC"})
            
            # List Area
            # ScrollView not implemented yet, so just a Box that grows
            self.list_container = ui.Box(style={"layout": "col", "gap": 10, "w": "100%"})
            root.add(self.list_container)

        app.add(root)
        app.run()

if __name__ == "__main__":
    todo = TodoApp()
    todo.build()

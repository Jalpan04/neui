"""
NEUI Text Wrapping Example - Demonstrates automatic text wrapping
"""
from neui import App, ui, cui

def build_app():
    app = App(title="NEUI Text Wrapping Demo", width=700, height=600)
    
    with ui.Box(style={
        "bg": "#0D1117",
        "w": "100%",
        "h": "100%",
        "padding": 30,
        "layout": "col",
        "gap": 20
    }) as root:
        
        # Header
        ui.Text("Text Wrapping Examples", style={
            "font_size": 28,
            "color": "#58A6FF",
            "weight": "bold"
        })
        
        # Example 1: No Wrapping (default)
        with cui.Card(style={
            "w": "100%",
            "bg": "#161B22",
            "padding": 20,
            "radius": 8,
            "layout": "col",
            "gap": 10
        }):
            ui.Text("No Wrapping (default)", style={
                "font_size": 16,
                "color": "#8B949E",
                "weight": "bold"
            })
            
            ui.Text(
                "This is a very long line of text that will not wrap and will extend beyond the container boundaries if it is too long.",
                style={
                    "font_size": 14,
                    "color": "#C9D1D9",
                    "wrap": "none"
                }
            )
        
        # Example 2: Word Wrapping
        with cui.Card(style={
            "w": "100%",
            "bg": "#161B22",
            "padding": 20,
            "radius": 8,
            "layout": "col",
            "gap": 10
        }):
            ui.Text("Word Wrapping", style={
                "font_size": 16,
                "color": "#8B949E",
                "weight": "bold"
            })
            
            ui.Text(
                "This is a demonstration of word wrapping in NEUI. The text will automatically wrap at word boundaries to fit within the specified width. This makes it much easier to create readable paragraphs without manually inserting line breaks.",
                style={
                    "font_size": 14,
                    "color": "#C9D1D9",
                    "wrap": "word",
                    "max_width": 600,
                    "line_height": 20
                }
            )
        
        # Example 3: Character Wrapping
        with cui.Card(style={
            "w": "100%",
            "bg": "#161B22",
            "padding": 20,
            "radius": 8,
            "layout": "col",
            "gap": 10
        }):
            ui.Text("Character Wrapping", style={
                "font_size": 16,
                "color": "#8B949E",
                "weight": "bold"
            })
            
            ui.Text(
                "Character-wrapping-breaks-at-any-character-boundary-which-can-be-useful-for-monospace-text-or-when-you-need-precise-control-over-line-breaks",
                style={
                    "font_size": 14,
                    "color": "#C9D1D9",
                    "wrap": "char",
                    "max_width": 500,
                    "line_height": 18
                }
            )
        
        # Example 4: Different Line Heights
        with cui.Card(style={
            "w": "100%",
            "bg": "#161B22",
            "padding": 20,
            "radius": 8,
            "layout": "col",
            "gap": 10
        }):
            ui.Text("Custom Line Height", style={
                "font_size": 16,
                "color": "#8B949E",
                "weight": "bold"
            })
            
            ui.Text(
                "You can control the line height for better readability. This text has a generous line height of 28 pixels, making it easier to read long paragraphs. Proper line height is important for good typography.",
                style={
                    "font_size": 14,
                    "color": "#C9D1D9",
                    "wrap": "word",
                    "max_width": 580,
                    "line_height": 28
                }
            )

    app.add(root)
    app.run()


if __name__ == "__main__":
    build_app()

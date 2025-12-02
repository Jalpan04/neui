"""
NEUI Form Example - Demonstrates all available form components
"""
from neui import App, ui, cui

class FormApp:
    def __init__(self):
        # Form state
        self.name_input = None
        self.email_input = None
        self.password_input = None
        self.newsletter_checkbox = None
        self.age_slider = None
        self.theme_toggle = None
        self.gender_radio = None
        self.result_text = None

    def on_submit(self):
        """Handle form submission"""
        # Gather form data
        name = self.name_input.text if self.name_input else "N/A"
        email = self.email_input.text if self.email_input else "N/A"
        
        # Get checkbox state
        newsletter = "Yes" if (self.newsletter_checkbox and self.newsletter_checkbox.checked) else "No"
        
        # Get slider value
        age = int(self.age_slider.value) if self.age_slider else 0
        
        # Get toggle state
        dark_mode = "Enabled" if (self.theme_toggle and self.theme_toggle.value) else "Disabled"
        
        # Get selected radio
        gender = "Not specified"
        if hasattr(self, 'male_radio') and self.male_radio.checked:
            gender = "Male"
        elif hasattr(self, 'female_radio') and self.female_radio.checked:
            gender = "Female"
        elif hasattr(self, 'other_radio') and self.other_radio.checked:
            gender = "Other"
        
        # Update result text
        if self.result_text:
            result = f"Name: {name}\nEmail: {email}\nNewsletter: {newsletter}\nAge: {age}\nDark Mode: {dark_mode}\nGender: {gender}"
            self.result_text.text = result
            print("\n=== FORM SUBMITTED ===")
            print(result)
            print("=====================\n")

    def on_clear(self):
        """Clear form fields"""
        if self.name_input:
            self.name_input.text = ""
            self.name_input.cursor_pos = 0
        if self.email_input:
            self.email_input.text = ""
            self.email_input.cursor_pos = 0
        if self.password_input:
            self.password_input.text = ""
            self.password_input.cursor_pos = 0
        if self.newsletter_checkbox:
            self.newsletter_checkbox.checked = False
        if self.age_slider:
            self.age_slider.value = 18
        if self.theme_toggle:
            self.theme_toggle.value = False
        if self.result_text:
            self.result_text.text = "Form cleared!"
        print("Form cleared!")

    def build(self):
        app = App(title="NEUI Form Example", width=600, height=800)
        
        with ui.Box(style={
            "bg": "#0D1117",
            "w": "100%",
            "h": "100%",
            "padding": 30,
            "layout": "col",
            "gap": 20,
            "align": "start"
        }) as root:
            
            # Header
            ui.Text("User Registration Form", style={
                "font_size": 32,
                "color": "#58A6FF",
                "weight": "bold"
            })
            
            ui.Text("Fill out the form below", style={
                "font_size": 14,
                "color": "#8B949E"
            })
            
            # Form Card
            with cui.Card(style={
                "w": "100%",
                "bg": "#161B22",
                "padding": 25,
                "radius": 8,
                "layout": "col",
                "gap": 20
            }):
                
                # Name Field
                ui.Text("Name", style={"font_size": 14, "color": "#C9D1D9", "weight": "bold"})
                self.name_input = ui.Input(
                    placeholder="Enter your name",
                    style={
                        "w": "100%",
                        "bg": "#0D1117",
                        "radius": 6,
                        "padding": 12,
                        "font_size": 14,
                        "color": "#C9D1D9"
                    }
                )
                
                # Email Field
                ui.Text("Email", style={"font_size": 14, "color": "#C9D1D9", "weight": "bold"})
                self.email_input = ui.Input(
                    placeholder="your.email@example.com",
                    style={
                        "w": "100%",
                        "bg": "#0D1117",
                        "radius": 6,
                        "padding": 12,
                        "font_size": 14,
                        "color": "#C9D1D9"
                    }
                )
                
                # Password Field
                ui.Text("Password", style={"font_size": 14, "color": "#C9D1D9", "weight": "bold"})
                self.password_input = ui.Input(
                    placeholder="Enter password",
                    password=True,
                    style={
                        "w": "100%",
                        "bg": "#0D1117",
                        "radius": 6,
                        "padding": 12,
                        "font_size": 14,
                        "color": "#C9D1D9"
                    }
                )
                
                # Checkbox
                with ui.Box(style={"layout": "row", "gap": 10, "align": "center"}):
                    self.newsletter_checkbox = cui.Checkbox(
                        style={"w": 20, "h": 20}
                    )
                    ui.Text("Subscribe to newsletter", style={"font_size": 14, "color": "#C9D1D9"})
                
                # Age Slider
                ui.Text("Age", style={"font_size": 14, "color": "#C9D1D9", "weight": "bold"})
                self.age_slider = cui.Slider(
                    min_val=18,
                    max_val=100,
                    value=25,
                    style={"w": "100%"}
                )
                
                # Toggle for Dark Mode
                with ui.Box(style={"layout": "row", "gap": 10, "align": "center"}):
                    ui.Text("Enable Dark Mode", style={"font_size": 14, "color": "#C9D1D9"})
                    self.theme_toggle = cui.Toggle(
                        value=True,
                        style={"w": 50, "h": 25}
                    )
                
                # Gender Radio Buttons
                ui.Text("Gender", style={"font_size": 14, "color": "#C9D1D9", "weight": "bold"})
                with ui.Box(style={"layout": "col", "gap": 10}):
                    with ui.Box(style={"layout": "row", "gap": 10, "align": "center"}):
                        self.male_radio = cui.Radio(group="gender", style={"w": 18, "h": 18})
                        ui.Text("Male", style={"font_size": 14, "color": "#C9D1D9"})
                    
                    with ui.Box(style={"layout": "row", "gap": 10, "align": "center"}):
                        self.female_radio = cui.Radio(group="gender", style={"w": 18, "h": 18})
                        ui.Text("Female", style={"font_size": 14, "color": "#C9D1D9"})
                    
                    with ui.Box(style={"layout": "row", "gap": 10, "align": "center"}):
                        self.other_radio = cui.Radio(group="gender", style={"w": 18, "h": 18})
                        ui.Text("Other", style={"font_size": 14, "color": "#C9D1D9"})
            
            # Buttons Row
            with ui.Box(style={"layout": "row", "gap": 15, "w": "100%"}):
                cui.Button(
                    "Submit",
                    on_click=self.on_submit,
                    style={
                        "w": 120,
                        "h": 40,
                        "bg": "#238636",
                        "radius": 6,
                        "font_size": 14
                    }
                )
                
                cui.Button(
                    "Clear",
                    on_click=self.on_clear,
                    style={
                        "w": 120,
                        "h": 40,
                        "bg": "#6E7681",
                        "radius": 6,
                        "font_size": 14
                    }
                )
            
            # Result Display
            with cui.Card(style={
                "w": "100%",
                "bg": "#161B22",
                "padding": 20,
                "radius": 8,
                "layout": "col",
                "gap": 10
            }):
                ui.Text("Form Data:", style={
                    "font_size": 16,
                    "color": "#58A6FF",
                    "weight": "bold"
                })
                
                self.result_text = ui.Text(
                    "Fill out the form and click Submit",
                    style={
                        "font_size": 12,
                        "color": "#8B949E"
                    }
                )

        app.add(root)
        app.run()


if __name__ == "__main__":
    form = FormApp()
    form.build()

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class MyApp(App):
    def build(self):
        self.counter = 0
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.label = Label(text=f"Button Pressed {self.counter} times", font_size=24)
        
        btn = Button(
            text="Press Me",
            font_size=20,
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5},
            background_color=[1, 1, 1, 1],  # Set background color to white
            color=[0, 0, 0, 1],             # Set text color to black
            background_normal="",           # Remove default background
        )
        
        # Bind the button press to an action
        btn.bind(on_press=self.on_button_press)
        
        # Add widgets to the layout
        layout.add_widget(self.label)
        layout.add_widget(btn)
        
        return layout

    def on_button_press(self, instance):
        self.counter += 1
        self.label.text = f"Button Pressed {self.counter} times"

if __name__ == "__main__":
    MyApp().run()
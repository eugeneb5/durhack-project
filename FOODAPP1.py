from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class FoodApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        title_label = Label(text="Food List", font_size=32, size_hint=(1, 0.2))
        
        # Input field for food name
        self.food_input = TextInput(
            hint_text="Enter a food type",
            size_hint=(1, 0.1),
            multiline=False
        )

        self.food_input.bind(on_text_validate=self.add_food_item)

        add_button = Button(
            text="Add Food",
            size_hint=(1, 0.1),
            background_color=[0.3, 0.6, 1, 1],
            color=[1, 1, 1, 1]
        )
        add_button.bind(on_press=self.add_food_item)

        self.food_list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.food_list_layout.bind(minimum_height=self.food_list_layout.setter('height'))
        
        scroll_view = ScrollView(size_hint=(1, 0.6))
        scroll_view.add_widget(self.food_list_layout)
        
        # Add widgets to the main layout
        main_layout.add_widget(title_label)
        main_layout.add_widget(self.food_input)
        main_layout.add_widget(add_button)
        main_layout.add_widget(scroll_view)
        
        return main_layout

    def add_food_item(self, instance):
        # Get food name from input field
        food_name = self.food_input.text.strip()
        
        if food_name:
            # Create a label for the new food item
            food_label = Label(
                text=food_name,
                font_size=20,
                size_hint_y=None,
                height=40
            )
            
            # Add the new food item to the layout
            self.food_list_layout.add_widget(food_label)
            
            # Clear the input field for the next entry
            self.food_input.text = ""

if __name__ == "__main__":
    FoodApp().run()

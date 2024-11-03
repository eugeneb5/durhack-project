from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from datetime import datetime
from datetime import date
import json
import requests




class FoodApp(App):

 
    def __init__(self, **kwargs):

        super(FoodApp, self).__init__(**kwargs)

        #self.food_list = []
        
        #self.checked = False
        self.urgency_dict = {}
        
        self.api_key = "9771b891aac744468cfd200a710fa6a3"

        self.food_dict= self.load_dict_file() # for any added foods - will have a key of food type etc...
        self.full_list = self.make_food_list()
        self.updated_list = self.full_list.copy() # start with the updated list as the full list
        self.data_bool = bool(self.food_dict)



    def build(self):   #note, .add_widget is position sensitive in the code, i.e. what is written first comes first


        title_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        title_label = Label(text="Food List", font_size=32, size_hint_x = 0.4)

        

        #add CHECK EXPIRY DATE button

        check_exp = Button(text = "CHECK FOOD EXPIRY NOW", size_hint_x = 0.3)
        check_exp.bind(on_press = self.expiry_data_check)

        save_button = Button(text = "Save Food List", size_hint_x = 0.3)
        save_button.bind(on_press = self.save_dictionary_to_file)

    

        title_layout.add_widget(title_label)
        title_layout.add_widget(save_button)
        title_layout.add_widget(check_exp)

        #main_layout.add_widget(check_exp)

        main_layout.add_widget(title_layout)


        self.search_input = TextInput(hint_text = "type in food item", size_hint = (1,0.1),multiline = False)

        self.search_input.bind(on_text_validate = self.update_list_) # bind allows us to call a function when search_input is called

        main_layout.add_widget(self.search_input)


        



    
       

        self.food_list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.food_list_layout.bind(minimum_height=self.food_list_layout.setter('height'))
        
        
        self.scroll_view = ScrollView(size_hint = (1,0.7))
        self.scroll_view.add_widget(self.food_list_layout)
        main_layout.add_widget(self.scroll_view)



        #if the txt file isn't empty at start, initialize save
        if self.data_bool:
            self.initialize()
        
        
       
        
        
        
        
        return main_layout



    def ingred_list(self):

        ingred = [i for i in self.urgency_dict]

        return ingred
    
    def find_recipes(self):
        ingredients = self.ingred_list()
        ingredient_query = ','.join(ingredients)

        url = 'https://api.spoonacular.com/recipes/findByIngredients' #SPOONACULAR AI
        
        

        params = {'ingredients': ingredient_query, 'number': 5, 'ranking': 1, 'ignorePantry': True, 'apiKey': self.api_key}  #note, ranking =1 tries to find the recipe with most used...

        response = requests.get(url, params=params)

        recipes = response.json()

        for r in recipes:

            title = r.get("title","no name - ERROR") # the second input is for fallback, if the value corresponding to that key couldnt be found..

            ingredient_compare = [i["name"] for i in recipe["used_ingredients"]] #searching in a dictionary within a dictionary!

            s = sum(self.urgency_dict.get(food_name[i],0) for food_name in ingredient_compare)

            print(f"Recipe: {title}")
            print(f"Total 'Value' of Used Ingredients: {total_value}") #the higher the better
            print("-" * 20)




        
    
    def load_dict_file(self):

        filename = 'saved_food_data.txt'
        try:
            with open(filename, 'r') as file:
                return json.load(file)  
        except FileNotFoundError:
            
            return {}  
    
    def save_dictionary_to_file(self, instance):

        filename = 'saved_food_data.txt'
        with open(filename, 'w') as file:
            json.dump(self.food_dict, file)
    
    def initialize(self):
        for food_name, details in self.food_dict.items():   #food_name refers to the key already, use details.get() to get expiry date...

            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40) #the master box...(includes food label, expiry date and remove button)
            
            #create and add food label to this...
            food_label = Label(text=food_name,font_size=20,size_hint_y=None,height=40)
            item_layout.add_widget(food_label)
            

            #adds expiry part
            exp_date = details.get("expiry date")
            expiry_label = Label(text=f"Expires on: {exp_date}", size_hint_x = 0.4, halign = 'left', valign='middle')
            expiry_label.bind(size = expiry_label.setter('text_size'))
            item_layout.add_widget(expiry_label)



            #put in remove button

            remove_button = Button(text="-", size_hint_x=0.2)
            remove_button.bind(on_press=lambda instance, name=food_name: self.remove_food_item(name))
            item_layout.add_widget(remove_button)


            self.food_list_layout.add_widget(item_layout)


    def expiry_data_check(self, instance):
        
        self.checked = True
        
        today_date = date.today()

        if not self.food_dict:
            print("Your list is empty!!!")
            return  #nothing, pass programme
        else:
            self.food_list_layout.clear_widgets()  #clear everything at the start again...
            for food_name, details in self.food_dict.items():

                exp_date = details.get("expiry date")

                exp_date = datetime.strptime(exp_date, "%Y-%m-%d").date()

                difference = exp_date - today_date
                if difference.days < 0:
                    item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
                    food_label = Button(text=food_name,font_size=20,size_hint_y=None,height=40, background_color = [0,0,0,1],color = [1,1,1,1],background_normal = "")
                    item_layout.add_widget(food_label)

                    expiry_label = Label(text="Throw it out now!", size_hint_x = 0.4, halign = 'left', valign='middle', color = [1,1,1,1])
                    expiry_label.bind(size = expiry_label.setter('text_size'))
                    item_layout.add_widget(expiry_label)

                elif difference.days  == 0:
                    self.urgency_dict[food_name] = 15 # arbitrary estimation of weighting, usually 15 things 
                    item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
                    food_label = Button(text=food_name,font_size=20,size_hint_y=None,height=40, background_color = [1,0,0,1],color = [1,1,1,1],background_normal = "")
                    item_layout.add_widget(food_label)

                    
                    expiry_label = Label(text=f"{difference.days} days left!!", size_hint_x = 0.4, halign = 'left', valign='middle', color = [1,1,1,1])
                    expiry_label.bind(size = expiry_label.setter('text_size'))
                    item_layout.add_widget(expiry_label)

                elif 0 < difference.days <= 2:
                    self.urgency_dict[food_name] = 7 #half of expiring stuff
                    item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
                    food_label = Button(text=food_name,font_size=20,size_hint_y=None,height=40, background_color = [1,0.5,0,0.5],color = [0,0,0,1],background_normal = "")
                    item_layout.add_widget(food_label)

                    expiry_label = Label(text=f"{difference.days} days left!", size_hint_x = 0.4, halign = 'left', valign='middle')
                    expiry_label.bind(size = expiry_label.setter('text_size'))
                    item_layout.add_widget(expiry_label)

                elif difference.days >= 3:
                    self.urgency_dict[food_name] = 1 #lowest priority.
                    item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
                    food_label = Button(text=food_name,font_size=20,size_hint_y=None,height=40, background_color = [0,1,0,0.5],color = [0,0,0,1],background_normal = "")
                    item_layout.add_widget(food_label)

                    expiry_label = Label(text=f"{difference.days} days left", size_hint_x = 0.4, halign = 'left', valign='middle')
                    expiry_label.bind(size = expiry_label.setter('text_size'))
                    item_layout.add_widget(expiry_label)
                
                remove_button = Button(text="-", size_hint_x=0.2)
                remove_button.bind(on_press=lambda instance, name=food_name: self.remove_food_item(name))
                item_layout.add_widget(remove_button)


                self.food_list_layout.add_widget(item_layout)
                

                    









                    
    
    def make_food_list(self):

        with open("FOOD.txt", "r") as file:
                food_list = [line.strip() for line in file if line.strip()] #strip removes the spaces and \n
        return food_list


    def expiry_date(self, instance):

        food_name = instance.text.strip()


        #the popup layout for entering expiry date:
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=f"Enter expiry date for {food_name} (YYYY-MM-DD):")
        self.expiry_input = TextInput(hint_text="YYYY-MM-DD", multiline=False)
        add_button = Button(text="Add", size_hint=(1, 0.3))
            
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(self.expiry_input)
        popup_layout.add_widget(add_button)

        #initializes the popup
        self.popup = Popup(title="Add Expiry Date", content=popup_layout, size_hint=(0.8, 0.4))
        add_button.bind(on_press = lambda x: self.add_food_item(food_name)) #or just use instance?
        self.popup.open()



    def add_food_item(self, food_name):
        # Get food name from input field
        #expiry_date = self.expiry_input.text.strip()
        #print(f"Expiry date: {expiry_date}")
        #print(food_name)
        #self.food_dict[food_name] = {"expiry date" : expiry_date} #is thuis updated properly?
        #expir_date = self.food_dict.get(food_name, {}).get("expiry date")
        #print(f"The expiry date for {food_name} is {expir_date}")
        #need to convert it to a datetime object later...

        

        try:
            expiry_date = datetime.strptime(self.expiry_input.text.strip(), "%Y-%m-%d").date()
        
     
            self.food_dict[food_name] = {"expiry date": expiry_date.strftime("%Y-%m-%d")}
        
        except ValueError:
        
            self.expiry_input.text = ""
            error_label = Label(text="Invalid date format! Use YYYY-MM-DD")
            self.popup.content.add_widget(error_label)
            
            #print("Invalid date format! Please enter in YYYY-MM-DD format. Press enter to continue...")
            #add kivy.clock to do a one second delay!!! please...

        
        
        self.popup.dismiss()
        #self.food_dict[food_name] = {"null"}
        self.food_list_layout.clear_widgets()
        
        for food_name, details in self.food_dict.items():   #food_name refers to the key already, use details.get() to get expiry date...

            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40) #the master box...(includes food label, expiry date and remove button)
            
            #create and add food label to this...
            food_label = Label(text=food_name,font_size=20,size_hint_y=None,height=40)
            item_layout.add_widget(food_label)
            

            #adds expiry part
            exp_date = details.get("expiry date")
            expiry_label = Label(text=f"Expires on: {exp_date}", size_hint_x = 0.4, halign = 'left', valign='middle')
            expiry_label.bind(size = expiry_label.setter('text_size'))
            item_layout.add_widget(expiry_label)



            #put in remove button

            remove_button = Button(text="-", size_hint_x=0.2)
            remove_button.bind(on_press=lambda instance, name=food_name: self.remove_food_item(name))
            item_layout.add_widget(remove_button)


            self.food_list_layout.add_widget(item_layout)


            # Clear the input field for the next entry
            self.search_input.text = ""

            self.updated_list = self.full_list.copy()
           
            #self.update_food_list_display()
    def update_list_(self, instance):  #we add instance since is outputted by .bind(text =)
         
         keep = instance.text.lower().strip()  #makes all lowercase and .strip() removes whitespace

         self.updated_list = [food for food in self.full_list if keep in food.lower()]


         self.update_food_list_display()
        
    def update_food_list_display(self):
         
         self.food_list_layout.clear_widgets() 

         for food in self.updated_list:
              
              food_button = Button(text=food, size_hint_y = None, height = 40)
              self.food_list_layout.add_widget(food_button)
              food_button.bind(on_press=self.expiry_date)
              
    def remove_food_item(self, food_name):
         
         if food_name in self.food_dict:
            del self.food_dict[food_name]
            self.food_list_layout.clear_widgets()
         for food_name in self.food_dict.keys():

            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            
            #create and add food label to this...
            food_label = Label(text=food_name,font_size=20,size_hint_y=None,height=40)
            item_layout.add_widget(food_label)

            #put in remove button

            remove_button = Button(text="-", size_hint_x=0.2)
            remove_button.bind(on_press=lambda instance, name=food_name: self.remove_food_item(name))
            item_layout.add_widget(remove_button)


            self.food_list_layout.add_widget(item_layout)


            # Clear the input field for the next entry
            self.search_input.text = ""

            self.updated_list = self.full_list.copy()

    
         
         
         
           
            
            
        
           
        
        
         
              
              
         
if __name__ == "__main__":
    FoodApp().run()

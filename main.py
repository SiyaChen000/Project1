import openai
from kivymd.uix.button import MDRaisedButton
from kivy.uix.floatlayout import FloatLayout
from pickle import FALSE
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Rotate
import time


Window.size = (410, 680)
screen_helper = """ 

#create different screen objects
ScreenManager:    
    IntroScreen: 
    MenuScreen: 
    InputInfoScreen: 
    HROLScreen: 
    TemperatureScreen: 
    EyeScanningScreen: 
    ResultsScreen: 
    HistoryScreen:

<IntroScreen>:   #blue introduction screen
    name: 'intro' 
    MDFloatLayout:  #Adjust size and color
        canvas.before: 
            Color: 
                rgba: 0.537, 0.812, 0.941, 1 
            Rectangle: 
                size: self.size 
                pos: self.pos 
        Image:   #background image
            source: "stethB.png" 
            pos_hint: {"center_x": .5, "center_y": .7} 
            size_hint: .6, .6 
        MDLabel:  #Text being displayed
            text: '"Because every little life deserves the best start."  ---SCJR Engineering' 
            halign: 'center' 
            pos_hint: {"center_x": .5, "center_y": .2} 
            font_size: '18sp' 
            font_name: 'Pangolin-Regular.ttf' 

<MenuScreen>: #Main menu of the app
    name: 'menu' 
    AnchorLayout: 
        anchor_x: 'center' 
        anchor_y: 'top' 
        MDTopAppBar:  #Top menu bar / title
            title: "Baby Diagnostic Tool" 
            md_bg_color: [0.502, 0, 0, 1]  

    BoxLayout: 
        orientation: 'vertical' 
        size_hint: 1, None 
        height: self.minimum_height 
        pos_hint:{'center_x': 0.5, 'top': 0.7} 
        padding: "10dp" 
        spacing: "30dp" 

        # Button for Input Information 
        MDRectangleFlatButton: 
            text: 'Input Information' 
            pos_hint: {'center_x':0.5,'center_y':0.7} 
            size_hint: None, None 
            size: "300dp", "50dp" 
            on_press: root.manager.current = 'inputinfo'    #When button is pressed, the app will switch to "input info" screen, see Line 135
            font_name: 'Pangolin-Regular.ttf'  
            font_size: '18sp' 
            text_color: 0, 0, 0, 1 
            md_bg_color: [1, 0.8, 0, 1]  # Yellow color 
            radius: [20,20,20,20]  # Rounded corners 

        # Button for Heart Rate & Oxygen Level 
        MDRectangleFlatButton: 
            text: 'Heart Rate & Oxygen Level Test' 
            pos_hint: {'center_x':0.5,'center_y':0.6} 
            size_hint: None, None 
            size: "300dp", "50dp" 
            on_press: root.manager.current = 'hrol' 
            font_name: 'Pangolin-Regular.ttf' 
            font_size: '18sp' 
            text_color: 0, 0, 0, 1 
            md_bg_color: [0.4, 0.8, 0.4, 1]  # Green color 
            radius: [20,20,20,20]  # Rounded corners 

        #Button for temperature 
        MDRectangleFlatButton: 
            text: 'Temperature Test' 
            pos_hint: {'center_x': 0.5, 'center_y':0.5} 
            size_hint: None, None 
            size: "300dp", "50dp" 
            on_press: root.manager.current = 'temperature' 
            font_name: 'Pangolin-Regular.ttf'  
            font_size: '18sp' 
            text_color: 0, 0, 0, 1 
            md_bg_color: [0.2, 0.6, 0.8, 1]  # Light Blue color 
            radius: [20,20,20,20]  # Rounded corners 

        # Button for Eye Scanning 
        MDRectangleFlatButton: 
            text: 'Eye Scanning' 
            pos_hint: {'center_x':0.5,'center_y':0.4} 
            size_hint: None, None 
            size: "300dp", "50dp" 
            on_press: root.manager.current = 'eyescanning' 
            font_name: 'Pangolin-Regular.ttf'  
            font_size: '18sp' 
            text_color: 0, 0, 0, 1 
            md_bg_color: [0.6, 0.3, 0.6, 1]  # Purple color 
            radius: [20,20,20,20]  # Rounded corners 


        MDRectangleFlatButton:
            text: 'Results'
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}  # Adjust center_y to make sure it appears
            size_hint: None, None
            size: "300dp", "50dp"
            on_press: root.manager.current = 'results'  # When pressed, navigate to results screen
            font_name: 'Pangolin-Regular.ttf'
            font_size: '18sp'
            text_color: 0, 0, 0, 1
            md_bg_color: [1, 0.4, 0.4, 1]  # Light Red 
            radius: [20, 20, 20, 20]  # Rounded corners

        # Button for History tab 
        MDRectangleFlatButton: 
            text: 'History' 
            pos_hint: {'center_x':0.5,'center_y':0.4} 
            size_hint: None, None 
            size: "300dp", "50dp" 
            on_press: root.manager.current = 'history' 
            font_name: 'Pangolin-Regular.ttf' 
            font_size: '18sp' 
            text_color: 0, 0, 0, 1 
            md_bg_color: [1, 0.4, 0.6, 1]  # Pink color 
            radius: [20,20,20,20]  # Rounded corners 

<InputInfoScreen>:   #Sub-screen for each test
    name: 'inputinfo' 
    MDLabel: 
        text: "Basic Information"   #Title of the page
        font_style: "H5" 
        halign: 'center' 
        pos_hint: {'center_x':0.5, 'center_y':0.9} 
    MDLabel: 
        text: "Progress: 1/4"    #progress track
        font_style: "Overline" 
        halign: 'center' 
        pos_hint: {'center_x':0.5, 'center_y':0.1} 
    MDLabel: 
        text: 'Please input your childs information below: ' 
        pos_hint: {'center_x':0.55,'center_y':0.8} 
    MyGrid: 
        pos_hint: {"center_x": 0.3, "center_y": 0.6} 
        size_hint: None, None 
        size: "280dp", "200dp" 
    MDRectangleFlatButton: 
        text: 'Confirm' 
        pos_hint: {'center_x': 0.5, 'center_y': 0.3} 
        on_press: root.manager.current = 'hrol'    #Nevigate to next test
        radius: [20, 20, 20, 20]  

    MDRectangleFlatButton: 
        text: 'Back' 
        pos_hint: {'center_x':0.5,'center_y':0.2} 
        radius: [20, 20, 20, 20]  
        on_press: app.go_back() 

<HROLScreen>: 
    name: 'hrol' 
    MDLabel: 
        text: "Heart Rate & oxygen Level" 
        font_style: "H5" 
        halign: 'center' 
        pos_hint: {'center_x':0.5, 'center_y':0.9} 
    MDLabel: 
        text: "Progress: 2/4" 
        font_style: "Overline" 
        halign: 'center' 
        pos_hint: {'center_x':0.5, 'center_y':0.1} 
    MDLabel: 
        text: 'Please place your childs finger on top of the sensor and wait for 30 seconds. Once the Confirm button turns green, you can proceed to the next test. ' 
        halign: 'center' 

     ######################################## 
    MDLabel: 
        id: countdown_label
        text: "Time remaining: 5s"  # Show the countdown
        font_style: "H5" 
        halign: 'center' 
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}

    MDRectangleFlatButton: 
        id: start_button
        text: 'Start'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}  
        on_press: root.start_timer()  # Start the countdown timer
        radius: [20, 20, 20, 20]

    MDRectangleFlatButton: 
        id: confirm_button
        text: 'Confirm' 
        pos_hint: {'center_x': 0.5, 'center_y': 0.3} 
        on_press: root.manager.current = 'temperature'   #nevigate to next test
        radius: [20, 20, 20, 20] 
    MDRectangleFlatButton: 
        text: 'Back' 
        pos_hint: {'center_x':0.5,'center_y':0.2} 
        size_hint: None, None 
        size: "300dp", "50dp" 
        radius: [20, 20, 20, 20]  
        on_press: app.go_back()    

<TemperatureScreen>: 
    name: 'temperature' 
    MDLabel: 
        text: "Temperature" 
        font_style: "H5" 
        halign: 'center' 
        pos_hint: {'center_x':0.5, 'center_y':0.9} 
    MDLabel: 
        text: "Progress: 3/4" 
        font_style: "Overline" 
        halign: 'center' 
        pos_hint: {'center_x':0.5, 'center_y':0.1} 
    MDLabel: 
        text: 'Please attach the temperature probe underneath your childs armpit, and wait for 30 seconds. Once the Confirm button turns green, you can proceed to the next test.' 
        halign: 'center' 

    MDLabel: 
        id: countdown_label
        text: "Time remaining: 5s"  # Show the countdown
        font_style: "H5" 
        halign: 'center' 
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}

    MDRectangleFlatButton: 
        id: start_button
        text: 'Start'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}  
        on_press: root.start_timer()  # Start the countdown timer
        radius: [20, 20, 20, 20]

    MDRectangleFlatButton: 
        id: confirm_button
        text: 'Confirm' 
        pos_hint: {'center_x': 0.5, 'center_y': 0.3} 
        on_press: root.manager.current = 'eyescanning' 
        radius: [20, 20, 20, 20]

    MDRectangleFlatButton: 
        text: 'Back' 
        pos_hint: {'center_x': 0.5, 'center_y': 0.2} 
        size_hint: None, None 
        size: "300dp", "50dp" 
        radius: [20, 20, 20, 20] 
        on_press: root.on_back_button_click()  

<EyeScanningScreen>: 
    name: 'eyescanning' 
    MDLabel: 
        text: "Eye Scanning" 
        font_style: "H5" 
        halign: 'center' 
        pos_hint: {'center_x':0.5, 'center_y':0.9} 
    MDLabel: 
        text: "Progress: 4/4" 
        font_style: "Overline"  
        halign: 'center' 
        pos_hint: {'center_x':0.5, 'center_y':0.1} 
    MDLabel: 
        text: 'Please take a clear photo of your childs eye and wait for 30 seconds. Once the Confirm button turns green, you can proceed to the next test' 
        halign: 'center' 
    MDRectangleFlatButton: 
        text: 'Back' 
        pos_hint: {'center_x':0.5,'center_y':0.2} 
        size_hint: None, None 
        size: "300dp", "50dp" 
        radius: [20, 20, 20, 20]  
        on_press: app.go_back() 

    MDRectangleFlatButton: 
        id: confirm_button
        text: 'Confirm' 
        pos_hint: {'center_x':0.5,'center_y':0.3} 
        size_hint: None, None 
        size: "300dp", "50dp" 
        radius: [20, 20, 20, 20]  
        on_press: root.manager.current = 'results'   #nevigate to next test  

    Camera:
        id: camera
        resolution: (640, 480)
        play: False #This will ensure camera is initially OFF
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        size_hint: None, None  # Don't let the camera scale automatically
        size: "180dp", "200dp"  # Size of the camera outline       
        canvas.before:
            PushMatrix
            Rotate:
                angle: -90
                origin: self.center
        canvas.after:
            PopMatrix

    ToggleButton:
        text: 'Turn on the camera' ## Turn on/off the camera
        on_press: root.toggle_camera()
        size_hint_y: None
        height: '48dp'
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}

    MDRectangleFlatButton:
        id: camera_capture
        text: 'Capture' 
        pos_hint: {'center_x': 0.5, 'center_y': 0.4} 
        size_hint: None, None 
        size: "300dp", "50dp" 
        radius: [20, 20, 20, 20]  
        on_press: root.capture()

<ResultsScreen>:
    name: 'results'
    MDRectangleFlatButton:
        text: 'Menu'
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        size_hint: None, None
        size: "300dp", "50dp"
        radius: [20, 20, 20, 20]
        on_press: root.manager.current = 'menu'


<HistoryScreen>:
    name: 'history'
    MDLabel:
        text: "Test History"
        font_style: "H5"
        halign: 'center'
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
    MDList:
        id: history_list
        size_hint_y: None
        height: "300dp"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}

    MDRectangleFlatButton: 
        text: 'Back' 
        pos_hint: {'center_x': 0.5, 'center_y': 0.2} 
        size_hint: None, None 
        size: "300dp", "50dp" 
        radius: [20, 20, 20, 20] 
        on_press: root.manager.current = 'menu'  # Go back to the main screen


"""


# Input information page (User input)
class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 2  # Column
        self.padding = 10
        self.spacing = 10

        # Add a label and text input for 'Name'
        self.add_widget(MDLabel(text="Name: ", halign="right"))  # Make sure the Name is next to the input box
        self.name_input = TextInput(multiline=False)  # This make sure user will only input one line of text
        self.add_widget(self.name_input)  # Add name_input into the widget so user can see it and interact with it

        # Add a label and text input for 'Age'
        self.add_widget(MDLabel(text="Age: ", halign="right"))
        self.age_input = TextInput(multiline=False)
        self.add_widget(self.age_input)  # Add age_input into the widget so user can see it and interact with it

        # Add a label and text input for 'Gender'
        self.add_widget(MDLabel(text="Gender: ", halign="right"))
        self.gender_input = TextInput(multiline=False)
        self.add_widget(self.gender_input)

        # Add a label and text input for 'Weight'
        self.add_widget(MDLabel(text="weight: ", halign="right"))
        self.weight_input = TextInput(multiline=False)
        self.add_widget(self.weight_input)


class MenuScreen(Screen):
    pass


class TemperatureScreen(Screen):
    countdown = 5  # Initial countdown time for testing
    timer_event = None

    def start_timer(self):
        """Starts the countdown timer."""
        self.ids.start_button.disabled = FALSE  # Disable the Start button
        # self.ids.start_button.md_bg_color = [0.8, 0.8, 0.8, 1]  # Set a neutral color when disabled
        self.ids.start_button.elevation = 0  # Remove shadow effect
        self.ids.start_button.shadow = False  # Explicitly remove shadow
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)  # Update every second

    def update_timer(self, dt):
        """Update the countdown timer every second."""
        self.countdown -= 1
        self.ids.countdown_label.text = f"Time remaining: {self.countdown}s"

        if self.countdown <= 0:
            # Stop the countdown when it reaches 0
            Clock.unschedule(self.timer_event)
            self.ids.confirm_button.disabled = False  # Enable the Confirm button
            self.ids.confirm_button.md_bg_color = [0.4, 0.8, 0.4, 1]  # Green color when enabled
            self.ids.confirm_button.elevation = 8  # Set normal elevation for Confirm button
            self.ids.confirm_button.shadow = True  # Add shadow to Confirm button when enabled

    def on_leave(self):
        """Reset the countdown when leaving the screen."""
        self.reset_timer()  # Reset the timer when leaving the screen

    def reset_timer(self):
        """Reset the countdown timer and stop the timer."""
        self.countdown = 5  # Reset countdown (can be changed for testing)
        self.ids.countdown_label.text = f"Time remaining: {self.countdown}s"  # Reset label text
        self.ids.start_button.disabled = False  # Enable the Start button
        self.ids.start_button.md_bg_color = [0.2, 0.6, 0.8, 1]  # Set Start button to normal color
        self.ids.start_button.elevation = 8  # Set normal elevation for Start button
        self.ids.start_button.shadow = True  # Add shadow when enabled
        self.ids.confirm_button.disabled = True  # Disable the Confirm button
        self.ids.confirm_button.md_bg_color = [0.8, 0.8, 0.8, 1]  # Set Confirm button to disabled color
        self.ids.confirm_button.elevation = 0  # Remove shadow for disabled Confirm button
        self.ids.confirm_button.shadow = False  # Explicitly remove shadow when disabled
        if self.timer_event:  # Only unschedule if the timer is running
            Clock.unschedule(self.timer_event)

    def on_back_button_click(self):
        """Handle back button press to reset the timer and navigate to the previous screen."""
        self.reset_timer()  # Reset the timer when the back button is clicked
        self.manager.transition.direction = "right"
        self.manager.current = self.manager.previous()  # Navigate to the previous screen, not always menu

    def on_confirm_button_click(self):
        """Handle confirm button press to reset the timer and navigate to the next screen."""
        self.reset_timer()  # Reset the timer when the confirm button is clicked
        self.manager.current = 'eyescanning'  # Navigate to the next screen (EyeScanning)


class EyeScanningScreen(Screen):
    camera = None
    camera_container = None

    # countdown = 5  # Initial countdown time for testing
    # timer_event = None

    def toggle_camera(self):
        camera = self.ids['camera']
        camera.play = not camera.play  # Toggle camera play state
        print(f"Camera play state: {camera.play}")

    def clear_input_field(self):
        """Clear all user input fields."""
        if hasattr(self.parent, 'root'):
            root = self.parent.root
            # Access MyGrid in the InputInfoScreen and clear its fields
            if hasattr(root, 'inputinfo') and root.inputinfo:
                input_screen = root.inputinfo
                input_screen.name_input.text = ""
                input_screen.age_input.text = ""
                input_screen.gender_input.text = ""
                input_screen.weight_input.text = ""

    def on_back_button_click(self):
        """Handle back button press to stop the camera and go back to the previous screen."""
        if self.camera:
            self.camera.play = False  # Stop the camera feed
        self.manager.transition.direction = "right"
        self.manager.current = self.manager.previous()  # Navigate to the previous screen

    def on_leave(self):
        """Stop the camera feed when leaving the screen."""
        if self.camera:
            self.camera.play = False

    def on_confirm_button_click(self):
        """Handle confirm button press to clear inputs, and navigate to the next screen."""
        self.reset_timer()  # Reset the timer when the confirm button is clicked
        self.clear_input_fields()  # Clear the input fields
        self.manager.current = 'history'  # Navigate to the history screen after

    # Inside your camera setup code
    def apply_camera_rotation(self, angle):
        # Apply the rotation directly to the camera widget
        with self.camera.canvas.before:
            # Clear previous rotation
            self.camera.canvas.before.clear()
            # Apply a rotation to the camera
            self.rotation = Rotate(angle=angle, origin=self.camera.center)

    def capture(self):
        '''Take Photo'''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class HROLScreen(Screen):
    countdown = 5  # Initial countdown time for testing
    timer_event = None

    def start_timer(self):
        """Starts the countdown timer."""
        self.ids.start_button.disabled = True  # Disable the Start button
        self.ids.start_button.md_bg_color = [0.8, 0.8, 0.8, 1]
        self.ids.start_button.elevation = 0  # Remove shadow effect
        self.ids.start_button.shadow = False
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)  # Update every second

    def update_timer(self, dt):
        """Update the countdown timer every second."""
        self.countdown -= 1
        self.ids.countdown_label.text = f"Time remaining: {self.countdown}s"

        if self.countdown <= 0:
            # Stop the countdown when it reaches 0
            Clock.unschedule(self.timer_event)
            self.ids.confirm_button.disabled = False  # Enable the Confirm button
            self.ids.confirm_button.md_bg_color = [0.4, 0.8, 0.4, 1]  # Green color when enabled
            self.ids.confirm_button.elevation = 8  # Set normal elevation for Confirm button
            self.ids.confirm_button.shadow = True


class InputInfoScreen(Screen):
    pass


class IntroScreen(Screen):
    pass


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)

        # Create a FloatLayout to control the placement
        layout = FloatLayout()

        # Label to display results
        self.result_label = MDLabel(text="Click the button to get a wellness evaluation.",
                                    halign="center", size_hint=(None, None), size=("280dp", "50dp"))
        self.result_label.pos_hint = {'center_x': 0.5, 'center_y': 0.7}  # Positioning label
        layout.add_widget(self.result_label)

        # Adding the 'Get Wellness Evaluation' button
        self.result_button = MDRaisedButton(text="Get Wellness Evaluation")
        self.result_button.size_hint = None, None
        self.result_button.size = "300dp", "50dp"
        self.result_button.radius = [20, 20, 20, 20]
        self.result_button.pos_hint = {'center_x': 0.5, 'center_y': 0.3}  # Change the vertical position
        self.result_button.bind(on_press=self.generate_wellness_evaluation)  # Binding button to function
        layout.add_widget(self.result_button)

        # Add the layout to the screen
        self.add_widget(layout)

    def generate_wellness_evaluation(self, instance):
        # Define the user data
        GENDER = "male"
        AGE = "1"
        WEIGHT = "20"
        TEMPERATURE = 104
        HEART_RATE_BPM = 90.98
        BLOOD_OXYGEN_LEVEL = 99
        EYE_COLOR = "NORMAL"

        # Create the prompt string for the GPT model
        prompt = f"""
        I want you to generate an overall wellness evaluation for me given some specific information and collected vitals. 
        The evaluation should be no more than 4 sentences and contain advice on my next best steps or if I should seek medical care. 
        The information collected is that I am {AGE} years old, {GENDER}, I weigh {WEIGHT} pounds. 
        My temperature is {TEMPERATURE} degrees Fahrenheit, my heart rate is {HEART_RATE_BPM}, 
        my blood oxygen level is {BLOOD_OXYGEN_LEVEL}%, and my sclera in my eye is a {EYE_COLOR} color. Say what you think it is and recommend to take them to the doctor if needed. " 
        Also please include what value is captured for each vital, display it like a list or table.
        """
        # If the child is healthy respond "Your child is healthy, keep visiting the doctor regularly."
        # Update the label text to indicate the process
        self.result_label.text = "Evaluating wellness... Please wait."

        # Get the wellness evaluation result from the GPT model
        evaluation = self.chat_with_gpt(prompt)

        # Update the label with the response from GPT
        self.result_label.text = evaluation

    def chat_with_gpt(self, prompt):
        # This method sends the prompt to GPT and returns the result
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Ensure the correct model is used
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Return the content of the response
        return response.choices[0].message['content']


class HistoryScreen(Screen):
    pass


class DemoApp(MDApp):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(IntroScreen(name='intro'))  # Ensure IntroScreen is added
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(TemperatureScreen(name='temperature'))
        sm.add_widget(EyeScanningScreen(name='eyescanning'))
        sm.add_widget(HROLScreen(name='hrol'))
        sm.add_widget(InputInfoScreen(name='inputinfo'))
        sm.add_widget(HistoryScreen(name='history'))

        screen = Builder.load_string(screen_helper)

        # Schedule transition to the menu screen after 5 seconds
        Clock.schedule_once(self.switch_to_menu, 5)

        return screen

    def switch_to_menu(self, dt):
        self.root.current = 'menu'

    def go_back(self):
        screen_manager = self.root
        previous_screen = screen_manager.previous()  # Get the previous screen
        if previous_screen != 'menu':  # Avoid looping back to menu if already there
            screen_manager.transition.direction = "right"
            screen_manager.current = previous_screen  # Go to the previous screen
        else:
            # You can set a custom behavior for navigating back to the menu if needed
            screen_manager.transition.direction = "right"
            screen_manager.current = "menu"


DemoApp().run()
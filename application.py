from turnitinAPI import main

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from functools import partial
import os

class MyGrid(GridLayout):

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)

        self.home()
    
    def home(self, instance=None):

        self.clear_widgets()

        self.cols = 2

        self.work = ''

        if os.stat("details.txt").st_size != 0:
            f = open('details.txt', 'r')
            

            lines = f.readlines()
            for line, text in enumerate(lines):
                if 'TurnitinEmail: ' in text:
                    self.work += main(text.split(':')[1].strip(), lines[line+1].split(':')[1])

            f.close()
        
        else:
            self.work = 'No platforms added'

        self.assignments = Label(text=self.work)
        self.add_widget(self.assignments)

        self.inside = GridLayout()
        self.inside.rows = 2
        self.add_widget(self.inside)
        
        self.turnLogin = Button(text='turnitin')
        self.inside.add_widget(self.turnLogin)
        self.turnLogin.bind(on_press=self.turnitinLogin)

        self.inside.add_widget(Button(text='canvas'))

    def turnitinLogin(self, instance):

        self.clear_widgets()

        self.inside = GridLayout()
        self.inside.cols = 2
        self.inside.rows = 2

        self.rows = 3
        self.cols = 1
        self.add_widget(self.inside)

        self.emailText = Label(text='Email')
        self.passwordText = Label(text='Password')
        self.inside.add_widget(self.emailText) 
        self.inside.add_widget(self.passwordText)

        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)
        self.password = TextInput(multiline=False)
        self.inside.add_widget(self.password)

        self.submit = Button(text='Submit')
        self.submit.bind(on_press=self.turnAPI)
        self.back = Button(text='Back')
        self.add_widget(self.submit)
        self.add_widget(self.back)
        self.back.bind(on_press=self.home)
    
    def turnAPI(self, instance):
        
        self.clear_widgets()

        self.cols = 1
        self.rows = 2
        self.exists = False
        f = open('details.txt', 'r')

        for i in f.readlines():
            if self.email.text in i:
                self.add_widget(Label(text='email already registered'))
                self.exists = True
                self.back = Button(text='Back')
                self.add_widget(self.back)
                self.back.bind(on_press=self.home)
                f.close()

        if main(self.email.text, self.password.text) != 'Wrong login' and self.exists == False:
            self.clear_widgets()
            self.add_widget(Label(text='Authenticated!'))
            f = open('details.txt', 'w')
            self.back = Button(text='Back')
            self.add_widget(self.back)
            self.back.bind(on_press=self.home)
            f.write(f'TurnitinEmail: {self.email.text}\n')
            f.write(f'Password: {self.password.text}')
            f.close()



class MyApp(App):

    def build(self):
        return MyGrid()

if __name__ == '__main__':
    MyApp().run()
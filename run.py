import asyncio
import threading

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from mochineko.discord_bot import main


class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        button = Button(text='Click Me')
        button.bind(on_press=self.runBot)
        text_area = TextInput(multiline=True)
        layout.add_widget(text_area)
        layout.add_widget(Label(text='Hello World'))
        layout.add_widget(button)
        return layout

    def runBot(self, instance):
        threading.Thread(target=self.start_bot, daemon=True).start()

    @staticmethod
    def start_bot():
        asyncio.run(main.main())

if __name__ == '__main__':
    MainApp().run()
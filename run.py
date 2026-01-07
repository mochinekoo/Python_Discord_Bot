import asyncio
import sys
import threading
from datetime import datetime
import codecs
from pathlib import Path

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.text import LabelBase, DEFAULT_FONT
from mochineko.discord_bot import main
import matplotlib.font_manager as fm

FONT_PATH = r""

class LogRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        if text.strip():
            Clock.schedule_once(lambda dt: self.update_text(text))

    def update_text(self, text):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text = text.strip().replace('\r\n', '\n').replace('\r', '\n')
        self.text_widget.text += f"[{timestamp}] {text}\n"

    def flush(self):
        pass

class MainApp(App):
    def build(self):
        global FONT_PATH
        fontList = fm.findSystemFonts()
        for font in fontList:
            if font.__contains__("msgothic"):
                FONT_PATH = font

        LabelBase.register(DEFAULT_FONT, FONT_PATH)
        layout = BoxLayout(orientation='vertical')

        self.text_area = TextInput(
            multiline=True,
            readonly=True,
            font_size='14sp',
            font_name=DEFAULT_FONT,
            text='',
        )
        
        layout.add_widget(self.text_area)
        
        status_label = Label(
            text='もちねこBot',
            font_name=DEFAULT_FONT,
            font_size='14sp'
        )
        layout.add_widget(status_label)

        button = Button(
            text='Botを起動',
            font_name=DEFAULT_FONT,
            font_size='14sp'
        )
        button.bind(on_press=self.runBot)
        layout.add_widget(button)

        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = LogRedirector(self.text_area)
        sys.stderr = LogRedirector(self.text_area)
        
        return layout

    def runBot(self, instance):
        instance.disabled = True
        instance.text = 'Bot Running'
        threading.Thread(target=self.start_bot, daemon=True).start()

    @staticmethod
    def start_bot():
        asyncio.run(main.main())

    def on_stop(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

if __name__ == '__main__':
    MainApp().run()
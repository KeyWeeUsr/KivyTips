# KV string /layouts only

# from kivy.app import runTouchApp
# from kivy.lang import Builder
# runTouchApp(Builder.load_string('''
# #:set rng range(4)
# #:import R random.random
# #:import Factory kivy.factory.Factory

# <RedButton@Button>:
#     background_color: (1, 0, 0, 0.5)

# BoxLayout:
#     RedButton:
#         id: rb
#         text: 'Simple kv string'
#         on_release:
#             self.parent.add_widget(Factory.Button())
#     Button:
#         text: 'Change color'
#         on_release:
#             rb.color = [R() for i in rng]
# '''))

# Widget with Python

# from kivy.app import runTouchApp
# from kivy.uix.label import Label
# from kivy.properties import StringProperty


# class MyLabel(Label):
#     my_text = StringProperty('Hi!')

#     def __init__(self, **kwargs):
#         super(MyLabel, self).__init__(**kwargs)
#         self.text = self.my_text
#         print(self.my_text)


# runTouchApp(MyLabel())

# Window config test (exit with escape)

# from kivy.config import Config
# Config.set('graphics', 'borderless', 1)
# Config.set('graphics', 'resizable', 0)
# from kivy.app import runTouchApp
# runTouchApp()

# loaders or separate methods

# from kivy.core.audio import SoundLoader
# from os.path import join, dirname
# from time import sleep
# import sys

# my_path = join(
#     dirname(sys.executable),
#     'share',
#     'kivy-examples',
#     'audio',
#     '12908_sweet_trip_mm_clap_hi.wav'
# )

# sound = SoundLoader.load(my_path)
# for i in range(10):
#     sound.play()
#     sleep(1)

# complex example

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label

Builder.load_string('''
#:set rng range(4)
#:import R random.random
#:import dp kivy.metrics.dp
<MyLabel>:
    font_size: dp(100)
    on_text:
        self.color = [R() for i in rng]
''')


class MyLabel(Label):
    def __init__(self, **kwargs):
        super(MyLabel, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.app.label = self


class Listener(Widget):
    def __init__(self, **kwargs):
        super(Listener, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.app.label.text = str(keycode)


class My(App):
    def build(self):
        self.listener = Listener()
        return MyLabel()


if __name__ == '__main__':
    My().run()

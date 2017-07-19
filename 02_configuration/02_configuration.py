# manipulate kivy configuration only
from kivy.config import Config
Config.set('graphics', 'height', 400)

# for loading config file
from os.path import exists, join, dirname, abspath
from ast import literal_eval

# casual kivy imports
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout


class MyConfigApp(App):
    # build app configuration only
    def build_config(self, config):
        # "MyConfig(App)"/"MyConfigApp(App)"
        #   -> "myconfig" .INI file
        conf_path = self.get_application_config()

        # load config from file if it exists
        if exists(conf_path):
            config.read(conf_path)
            return

        # create a separate "Config" for application only
        # with a separate config file placed to locations
        # mentioned in App.get_application_config
        config.setdefaults('my_config', {
            'layout': 'BoxLayout',  # real class name
            'child': 'Button',      # real class name
            'text_values': [
                'Hi', 'from', 'the', 'config', '!'
            ]
        })

        # nope, kivy config needed!
        config.setdefaults('graphics', {
            'height': 2000
        })

    def build(self):
        # get app configuration
        # it's still available via self.config no matter if
        # you use build_config or not i.e. you can create
        # the sections, set&get values and more anyway
        app_config = self.config

        # get the layout class' strings and text_values from config
        layout_str = app_config.get('my_config', 'layout')
        child_str = app_config.get('my_config', 'child')

        # to get a real list instead of "['val1', 'val2']"
        text_values = literal_eval(
            app_config.get('my_config', 'text_values')
        )

        # pull real classes from imported modules via config str
        # ! the classes mentioned in the config have to be already
        # ! imported when these lines are executing
        layout_cls = globals()[layout_str]
        child_cls = globals()[child_str]

        # create instance for the layout with some properties
        layout = layout_cls(
            orientation='vertical',
            pos_hint={
                'center_x': 0.5,
                'center_y': 0.5
            },
            size_hint=(0.5, 0.5)
        )

        for value in text_values:
            layout.add_widget(child_cls(text=value))

        layout.add_widget(Label(text=str(
            self.config == Config
        )))
        layout.add_widget(Label(text='app: ' + str(self.config)))
        layout.add_widget(Label(text='kivy: ' + str(Config)))
        return layout


if __name__ == '__main__':
    MyConfigApp().run()

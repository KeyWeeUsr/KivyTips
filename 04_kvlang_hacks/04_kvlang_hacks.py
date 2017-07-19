from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.uix.boxlayout import BoxLayout
runTouchApp(Builder.load_string('''
#:include kvext.kv

#:import Factory kivy.factory.Factory
#:import r random.random
#:set d round

BoxLayout:
    GridLayout:
        cols: 5
        id: grid
    Button:
        text: 'clear grid'
        on_release:
            grid.clear_widgets()
    Button:
        text: 'add FW'
        on_release:
            grid.add_widget(Factory.ForWidget())
    Button:
        text: '_forw'
        on_release:
            _forw(grid, 6, Factory.Button)
    Button:
        text: '_forws'
        on_release:
            _forws(grid, [
            [Factory.Spinner, {'values':[str(x) for x in range(5)]}],
            [Factory.Button, {'text':'blob'}],
            [Factory.Label, {'color': (1, 0, 0, 1), 'text':'blob'}]
            ])
    Widget:
    BoxLayout:
        orientation: 'vertical'
        Button:
            id: id_a
            text: 'a'
        Button:
            id: id_b
            text: 'b'
        Button:
            id: id_c
            text: 'c'
        Button:
            id: id_d
            text: 'd'
        BoxLayout:
            orientation: 'vertical'
            Button:
                text: 'swap a<->d'
                on_release: _swapw(id_a, id_d)
            Button:
                text: 'swap b<->c'
                on_release: _swapw(id_b, id_c)

<ForWidget@ButtonBehavior+Label>:
    on_parent: self.dummy += 1
    dummy: 0
    on_dummy: if self.dummy <= 2: _forw(self.parent, 6, Factory.Button)
'''))

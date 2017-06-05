from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

# This part is here only for the video
READABLE_IDS = True
WORDS = [
    'red', 'pony', 'knife', 'whistle', 'tree',
    'green', 'hamster', 'broom', 'ball', 'root'
]


# class with a shared kivy property
class MyButton(Button):
    # force_dispatch is needed in cases when the property
    # already holds its local value, yet the rest of the
    # instances don't, therefore without it it won't
    # trigger the on_* event -> no broadcast/update
    shared_value = StringProperty(force_dispatch=True)
    _instances = []

    # private to forbid changing the state from outside
    __shared = False

    def __init__(self, shared=False, readable=None, **kwargs):
        # for video
        self.readable = readable

        # real fun begins!
        super(MyButton, self).__init__(**kwargs)

        # if not shared, don't broadcast to other instances
        if not shared:
            self.text = "I don't have a shared value!"
            return

        # get app instance to lock the broadcasting later
        # only one instance can broadcast at the time
        self.app = App.get_running_app()

        # if shared, add to the class list of instances
        self.__shared = True
        MyButton._instances.append(self)

        # create a dictionary for global broadcast
        # locks if it doesn't exist, otherwise ignore
        if 'shared_value' not in self.app._locks:
            self.app._locks['shared_value'] = {
                'queue': [],
                'current': None,
                'check': Clock.schedule_interval(
                    MyButton.check_queue, 1
                )
            }

    @property
    def shared(self):
        return self.__shared

    def on_shared_value(self, instance, value):
        # ignore event if the instance isn't marked
        # as an instance holding a shared property
        if not self.shared:
            return

        # ignore changes from other instances
        # while broadcasting the same value
        if value == self.app._locks['shared_value']['current']:
            return

        # append the new value to the queue
        self.app._locks['shared_value']['queue'].append(value)

    @staticmethod
    def check_queue(*args):
        app = App.get_running_app()
        if 'lock' in app._locks['shared_value']:
            return

        # return if there's nothing in the queue
        if not app._locks['shared_value']['queue']:
            return

        # pop a new value from the queue
        # and update all instances with it
        broadcast = app._locks['shared_value']['queue'].pop(0)
        app._locks['shared_value']['current'] = broadcast

        # start broadcasting
        app._locks['shared_value']['lock'] = Clock.schedule_interval(
            lambda *dt: MyButton.update_values(broadcast), 0
        )

    # broadcasting method
    @staticmethod
    def update_values(value):
        app = App.get_running_app()

        # copy values somewhere in case the original
        # _instances is updated while broadcasting
        if not hasattr(MyButton, '_instances_temp'):
            MyButton._instances_temp = MyButton._instances[:]

        button = MyButton._instances_temp.pop()
        button.shared_value = value

        # just visual, the "shared_value" change is important
        button.text = value

        if not MyButton._instances_temp:
            # unschedule event and release the lock
            # (allow fetching another item from queue)
            Clock.unschedule(app._locks['shared_value']['lock'])
            del MyButton._instances_temp
            del app._locks['shared_value']['lock']

            # reset current value, allow appending
            # the released value to the queue
            app._locks['shared_value']['current'] = None

    # update the property with click/touch to stringified
    # instance value ("self"). This isn't necessary and a simple
    # "<instance>.property = value" is just fine, but this way
    # it's easier for showcasing
    def on_release(self):
        new_value = 'Click here! ' + str(self)[-11:-1]

        self.shared_value = new_value if not READABLE_IDS else self.readable


class PropertyBroadcasting(App):
    def build(self):
        # locks for property broadcasting
        self._locks = {}

        layout = BoxLayout(orientation='vertical')
        for i in range(10):
            for share in (False, True):
                # for video
                readable = WORDS.pop() if READABLE_IDS and share else ''

                box = BoxLayout()
                button = MyButton(
                    text='Click here!' if share else '',
                    shared=share,
                    readable=readable
                )
                box.add_widget(button)

                text = str(button)[-11:-1]
                text = readable if READABLE_IDS and share else text

                box.add_widget(Button(
                    text=text,
                    disabled=True
                ), index=1)
                layout.add_widget(box)
        return layout


if __name__ == '__main__':
    PropertyBroadcasting().run()

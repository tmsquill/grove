from functools import partial

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '800')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line
from pymongo import MongoClient
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.properties import AliasProperty

connection = MongoClient('localhost', 27017)
simulations = connection['grove']['simulations']

simulation = simulations.find()[0]

step = float(Window.size[0]) / 20


class Grid(Widget):

    origin_x = NumericProperty(0.0)
    origin_y = NumericProperty(0.0)

    def get_origin(self):

        return (self.origin_x, self.origin_y)

    def set_origin(self, value):

        self.origin_x = value[0]
        self.origin_y = value[1]

    origin = AliasProperty(get_origin, set_origin, bind=('origin_x', 'origin_y'))

    def __init__(self, **kwargs):

        super(Grid, self).__init__(**kwargs)

        self.bind(
            size=self.redraw,
            origin=self.redraw,
        )

    def redraw(self, *args):

        self.canvas.clear

        with self.canvas:

            width = self.parent.width
            height = self.parent.height

            x0 = self.origin[0]
            y0 = self.origin[1]

            # verticals
            number_of_lines = int(width / step)

            current_x = (x0 % step)
            delta_x = current_x - x0
            dashed = bool(delta_x % 100)
            for i in range(number_of_lines):
                if dashed:
                    Color(1, 1, 1, 1)
                    Line(
                        points=(current_x, 0, current_x, height),
                        width=1,
                        dash_length=10,
                        dash_offset=10,
                    )
                else:
                    Color(127./255, 127./255, 127./255, 0.5)
                    Line(points=(current_x, 0, current_x, height), width=1)

                dashed = not dashed
                current_x += step
                delta_x += step

            # draw origin y axis
            # Color(114/255, 159/255, 207/255, 1)
            Color(1, 1, 1)
            Line(points=(x0, 0, x0, height), width=1)

            # horizontals
            number_of_lines = int(height / step) + 1  # XXX: without + 1 top line is missing

            current_y = (y0 % step)
            delta_y = current_y - y0
            dashed = bool(delta_y % 100)
            for i in range(number_of_lines):
                Color(1, 1, 1, 1)
                if dashed:
                    Line(
                        points=(0, current_y, width, current_y),
                        width=1,
                        dash_length=10,
                        dash_offset=10,
                    )
                else:
                    Color(127./255, 127./255, 127./255, 0.5)
                    Line(points=(0, current_y, width, current_y), width=1)
                    # this can be avoided

                dashed = not dashed
                current_y += step
                delta_y += step

            # draw origin x axis
            Color(1, 1, 1)
            Line(points=(0, y0, width, y0), width=1)

        for child in self.children:
            self.canvas.add(child.canvas)


class LyssaApp(App):

    timestep = 0

    def update(self, widget, label, *largs):

        widget.canvas.clear()

        label.text = 'Timestep: ' + str(LyssaApp.timestep)

        global simulation
        entities = filter(lambda x: x[0] == LyssaApp.timestep, simulation.values()[0])

        with widget.canvas:

            for entity in entities:

                if entity[1] == u'SimAgent':

                    print 'SimAgent'
                    Color(float(209) / 256, float(73) / 256, float(5) / 256)

                elif entity[1] == u'Food':

                    print 'Food'
                    Color(float(125) / 256, float(140) / 256, float(31) / 256)

                elif entity[1] == u'Nest':

                    print 'Nest'
                    Color(float(66) / 256, float(126) / 256, float(147) / 256)

                else:

                    raise ValueError('Invalid entity type:', entity[1])

                print entity

                entity_pos = ((float(entity[5]) * step), (float(entity[6]) * step))
                entity_size = (step * abs(entity[5] - entity[7]), step * abs(entity[6] - entity[8]))

                Rectangle(pos=entity_pos, size=entity_size)

    def next_timestep(self, widget, label, *largs):

        # TODO

        LyssaApp.timestep += 1

        self.update(widget, label, *largs)

    def previous_timestep(self, widget, label, *largs):

        if LyssaApp.timestep > 0:

            LyssaApp.timestep -= 1

        self.update(widget, label, *largs)

    def build(self):

        widget = Widget()

        label = Label(text='Timestep: 0')

        nt = Button(text='Next', on_press=partial(self.next_timestep, widget, label))
        pt = Button(text='Previous', on_press=partial(self.previous_timestep, widget, label))

        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(nt)
        layout.add_widget(pt)
        layout.add_widget(label)

        root = BoxLayout(orientation='vertical')
        root.add_widget(Grid(origin=(float(Window.width) / 2, float(Window.height) / 2)))
        root.add_widget(widget)
        root.add_widget(layout)

        return root

if __name__ == '__main__':

    LyssaApp().run()

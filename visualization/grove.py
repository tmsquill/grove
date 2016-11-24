
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.widget import Widget

from pymongo import MongoClient

from simulation.entity import SimAgent, Food, Nest

connection = MongoClient('localhost', 27017)
evolutions = connection['grove']['evolutions']


class SimulationCanvas(Widget):

    def update(self, *args):

        simulation = GroveApp.sim
        simulation.execute_step()

        step = float(self.height / 20)
        self.canvas.clear()

        with self.canvas:

            for entity in reversed(simulation.entities):

                if isinstance(entity, SimAgent):

                    if entity.holding_food:

                        Color(float(209) / 256, float(73) / 256, float(5) / 256)

                    else:

                        Color(float(255) / 256, float(0) / 256, float(0) / 256)

                elif isinstance(entity, Food):

                    Color(float(125) / 256, float(140) / 256, float(31) / 256)

                elif isinstance(entity, Nest):

                    Color(float(66) / 256, float(126) / 256, float(147) / 256)

                else:

                    raise ValueError('Invalid entity type:', type(entity))

                x_tl = entity.body.top_left.position[0]
                y_tl = entity.body.top_left.position[1]
                x_br = entity.body.bottom_right.position[0]
                y_br = entity.body.bottom_right.position[1]

                entity_pos = ((float(x_tl) * step), (float(y_tl) * step))
                entity_size = (step * abs(x_tl - x_br), step * abs(y_tl - y_br))

                Rectangle(pos=entity_pos, size=entity_size)


class GroveApp(App):

    sim = None

    def build(self):

        self.load_simulation()

        sim_can = SimulationCanvas()

        root = BoxLayout(orientation='vertical')
        root.add_widget(sim_can)

        Clock.schedule_interval(sim_can.update, 0.25)

        return root

    def load_simulation(self):

        object_id = '58333b82816b6b05dc6b815a'
        generation_idx = 0
        agent_idx = 5

        from bson.objectid import ObjectId

        global evolitions
        evolution = evolutions.find_one({"_id": ObjectId(object_id)})
        active = evolution['generations'][generation_idx][agent_idx]

        generation = active[0]
        genome = active[1]
        value = active[2]
        random_seed = active[3]

        from grammar.grammar import Grammar
        from grammar.parse_tree import ParseTree
        from simulation.environment import Environment
        from simulation.simulation import Simulation
        from simulation.utils import rand

        import random

        grammar = Grammar('/Users/Zivia/Research/grove-examples/cpfa_ges/thrift/foraging.thrift')
        root = ParseTree(grammar, genome)
        root.generate()

        print root.root.obj

        rand = random.Random(random_seed)

        # Create the entities for the simulation.
        agents = [SimAgent(position=(rand.randint(8, 11), rand.randint(8, 11))) for _ in xrange(5)]
        nest = Nest(position=(8, 8), size=(4, 4))
        food = [Food(position=(rand.choice([rand.randint(0, 7), rand.randint(12, 20)]), rand.choice([rand.randint(0, 7), rand.randint(12, 20)]))) for _ in xrange(80)]

        entities = agents + [nest] + food

        # Create the environment for the simulation.
        env = Environment()

        # Create and execute the simulation.
        GroveApp.sim = Simulation(environment=env, entities=entities, parse_tree=root.root.obj)


if __name__ == '__main__':

    GroveApp().run()

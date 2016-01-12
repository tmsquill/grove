import os

from evolution.agent import ARGoSAgent
import evolution.config as config
import evolution.ga as ga
import evolution.selection as selection
import evolution.crossover as crossover
import evolution.mutation as mutation


class ForagerAgent(ARGoSAgent):

    def __init__(self):

        super(ForagerAgent, self).__init__()
        self.xml_argos = None

    @staticmethod
    def factory():

        return ForagerAgent()

    # TODO: Maybe remove this.
    def evaluate(self, argos_xml):

        pass


def pre_evaluation(agent):

    pass


def post_evaluation():

    pass


if __name__ == "__main__":

    import argparse

    # Parser for command line arguments.
    parser = argparse.ArgumentParser(description='py.evolve')
    parser.add_argument('-agent_config', action='store', type=str, default='./experiments/agent.json')
    parser.add_argument('-ga_config', action='store', type=str, default='./experiments/ga.json')
    parser.add_argument('-p', '--population', action='store', type=int, default=20)
    parser.add_argument('-g', '--generations', action='store', type=int, default=3)
    parser.add_argument('-c', '--crossover_function', action='store', type=str, default='truncation')
    parser.add_argument('-m', '--mutation_function', action='store', type=str, default='one_point')
    parser.add_argument('-s', '--selection_function', action='store', type=str, default='gaussian')
    args = parser.parse_args()

    # Change the current directory to ARGoS (required by the simulator).
    os.chdir(os.path.expanduser('~') + '/ARGoS/iAnt-GES-ARGoS')

    # Load the configurations into memory (as dictionaries) by filename.
    config.load_configs([args.agent_config, args.ga_config])

    # Run the genetic algorithm.
    ga.evolve(
        args.population,
        args.generations,
        ForagerAgent,
        '/bin/echo',
        selection.tournament(4, 5),
        crossover.one_point(),
        mutation.gaussian(),
        'log'
    )

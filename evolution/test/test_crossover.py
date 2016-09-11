from evolution.agent import Agent
from grove import config

import evolution.crossover as crossover


config.load_config('evolution/test/grove-config.json')


def test_one_point():

    agents = [Agent() for _ in xrange(10)]
    agents = crossover.one_point()(agents=agents, population=20)

    assert len(agents) == 20


def test_two_point():

    agents = [Agent() for _ in xrange(10)]
    agents = crossover.two_point()(agents=agents, population=20)

    assert len(agents) == 20


def test_uniform():

    agents = [Agent() for _ in xrange(10)]
    agents = crossover.uniform()(agents=agents, population=20)

    assert len(agents) == 20

from evolution.agent import Agent
from grove import config

import evolution.mutation as mutation


config.load_config('evolution/test/grove-config.json')


def test_truncation():

    agents = [Agent() for _ in xrange(10)]
    agents = mutation.boundary(agents)

    assert len(agents) == 10


def test_tournament():

    agents = [Agent() for _ in xrange(10)]
    agents = mutation.gaussian(agents)

    assert len(agents) == 10


def test_roulette():

    agents = [Agent() for _ in xrange(10)]
    agents = mutation.uniform(agents)

    assert len(agents) == 10

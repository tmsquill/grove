from evolution.agent import Agent
from grove import config

import evolution.selection as selection


config.load_config('evolution/test/grove-config.json')


def test_truncation():

    agents = [Agent() for _ in xrange(10)]
    agents = selection.truncation(0.2)(agents)

    assert len(agents) == 2


def test_tournament():

    agents = [Agent() for _ in xrange(10)]
    agents = selection.tournament(2, 3)(agents)

    assert len(agents) == 2


def test_roulette():

    pass

===================================
Fuzzy String Matching
===================================

This example demonstrates the core usage of Grove through a simple genetic algorithm optimizing strings to match a
target string. This is done with a fuzzy approach that provides the means necessary to determine partial success, which
is needed by the genetic algorithm to optimize.

Grove Configuration
===================

The next step is to specify the grove-config.json file loaded by Grove for determining specific
configuration options.

.. literalinclude:: /../../grove-examples/fuzzy_string_matching/grove-config.json

Main
====

We finally are able to put all of the pieces together and directly interface with Grove. In the main.py file we:

- Extend the :class:`~grove.evolution.agent.Agent` class to provide functionality for parse trees.
- Define an initialization method for the population.
- Define pre-evaluation, evaluation, and post-evaluation function. In this case, pre-evaluation will generate parse
  trees for all agents, serialize them, and place the result in the payload attribute of the agent. Evaluation runs
  the simulation. Note that post-evaluation is not needed for this example.

Lastly, we perform all necessary setup, then call Grove to start evolution.

.. literalinclude:: /../../grove-examples/fuzzy_string_matching/main.py

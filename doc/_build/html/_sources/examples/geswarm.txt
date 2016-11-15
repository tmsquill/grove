===================================
GESwarm - Recreating a Generic CPFA
===================================

GESwarm is a concrete use case of grammatical evolution. It uses a formal grammar
to specify the set of all possible rules that dictate the collective behaviors
manifested in a simulation. Derivations of the grammar are then evolved, which correlate
directly with state machines used by the simulator. For this example, we will use an
incredibly simple 2D simulator included with Grove.

For more information about this problem, see :ref:`refGESwarm`.

Formal Grammar
==============

To perform grammatical evolution, we need to specify a formal grammar. Currently, Grove supports
three representations of formal grammars - Apache Thrift, BNF, and FlatBuffers. Here we choose
Apache Thrift, although the other options would be just as usable.

The specification provided by GESwarm concisely describes the formal grammar. At the top level,
there exists an arbitrary list of rules. Each rule consists of an arbitrary list of preconditions,
behaviors, and actions. Each precondition, behavior, and action contain a terminal symbol.

.. literalinclude:: /../../grove-examples/cpfa_ges/thrift/foraging.thrift

Grove Configuration
===================

The next step is to specify the grove-config.json file loaded by Grove for determining specific
configuration options.

.. literalinclude:: /../../grove-examples/cpfa_ges/grove-config.json

Main
====

We finally are able to put all of the pieces together and directly interface with Grove. In the main.py file we:

- Extend the :class:`~grove.evolution.agent.Agent` class to provide functionality for parse trees.
- Define an initialization method for the population.
- Define pre-evaluation, evaluation, and post-evaluation function. In this case, pre-evaluation will generate parse
  trees for all agents, serialize them, and place the result in the payload attribute of the agent. Evaluation runs
  the simulation. Note that post-evaluation is not needed for this example.

Lastly, we perform all necessary setup, then call Grove to start evolution.

.. literalinclude:: /../../grove-examples/cpfa_ges/main.py

.. _refGESwarm:

Reference
=========

*Ferrante, Eliseo, et al. "GESwarm: Grammatical evolution for the automatic synthesis of collective behaviors in swarm
robotics." Proceedings of the 15th annual conference on Genetic and evolutionary computation. ACM, 2013.*

# Grove #

[![Build Status](https://travis-ci.org/zivia/grove.svg?branch=master)](https://travis-ci.org/zivia/grove)

Grove is a genetic algorithm and grammatical evolution library.

### Features ###

* Generic template for evolving agent based models.
* [Grammatical Evolution](https://en.wikipedia.org/wiki/Grammatical_evolution) supporting popular formal grammar representations such as BNF, Google Protocol Buffers, and Apache Thrift.
* Distributed execution of evaluation functions and grammar-related procedures.
* Extensive logging and output files for data analysis.

### Installation ###

The preferred method for installing Grove is [easy_install](https://pypi.python.org/pypi/setuptools) or
[pip](http://www.pip-installer.org/en/latest/).

```bash
easy_install grove
```

or

```bash
pip install grove
```

Alternatively, you can [download](https://pypi.python.org/pypi/grove/) or [clone](https://github.com/zivia/grove.git)
the repository and build from sources.

```bash
python setup.py install
```

Grove also optionally uses the [ETE Toolkit](http://etetoolkit.org/) for graphing parse trees generated during
grammatical evolution. Installation through [conda](http://conda.pydata.org/docs/) is required to use this feature.

```bash
conda install grove
```

### Documentation ###

Check the Grove User's Guide for documentation and examples.

### Contribution ###

Please fork and submit a pull request if you've created a feature that you think should be added.

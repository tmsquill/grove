from setuptools import setup, find_packages

setup(
    name='grove',
    version='0.0.1',
    url='https://github.com/zivia/grove',
    author='Troy Squillaci',
    author_email='troysquillaci@gmail.com',
    description='Genetic algorithm and grammatical evolution library.',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    license='MIT',
    install_requires=[]
)

from setuptools import setup

#with open('requirements.txt') as f:
#    required = f.read().splitlines()

setup(
    name="nb_quality_profile",
    packages=['nb_quality_profile'],
    version='0.2.4',
    author="Tony Hirst",
    author_email="tony.hirst@gmail.com",
    description="Tools for profiling Jupyter notebook quality and visualing notebook structure.",
    long_description='''
    A range of tools for profiling Jupyter notebooks and visualising notebook structure.
    ''',
    long_description_content_type="text/markdown",
    install_requires=["nbformat", "jupytext", "click",
                      "deepmerge", "lxml", "markdown",
                      "matplotlib", "spacy", "textacy", "readtime",
                      "list-imports", "pytest-codeblocks", "radon"],
    entry_points='''
        [console_scripts]
        nb_quality=nb_quality_profile.cli:cli
    '''

)

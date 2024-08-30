from setuptools import setup

# with open('requirements.txt') as f:
#    required = f.read().splitlines()

setup(
    name="nb_quality_profile",
    packages=["nb_quality_profile"],
    version="0.3.1",
    author="Tony Hirst",
    author_email="tony.hirst@gmail.com",
    description="Tools for profiling Jupyter notebook quality and visualing notebook structure.",
    long_description="""
    A range of tools for profiling Jupyter notebooks and visualising notebook structure.
    """,
    long_description_content_type="text/markdown",
    install_requires=[
        "nbformat", "isort",
        "jupytext",
        "click",
        "deepmerge",
        "lxml",
        "markdown",
        "pandas==2.2.1",
        "matplotlib==3.7.5","numpy<2",
        "spacy==3.7.5",
        "scikit-learn==1.3.2", "scipy==1.11.4",
        "readtime",
        "list-imports",
        "pytest-codeblocks",
        "radon", "pyflakes"
    ],
    entry_points="""
        [console_scripts]
        nb_quality=nb_quality_profile.cli:cli
    """,
)

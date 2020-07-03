# nb\_quality\_profile
Simple tools for reviewing the quality of Jupyter notebooks.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/innovationOUtside/nb_quality_profile/master?filepath=demo.ipynb)

At the moment, only a single tool is provided: a visualisation of notebook structure (relative length, structure in terms of markdown vs code cell). Visualisations are of the form:

![](.images/simple_nb_viz.png)

## Installation

Install from this repo:

`pip install git+https://github.com/innovationOUtside/nb_quality_profile.git`

## Usage

On the command line, cd to the desired directory and run:

`nb_quality .`

or pass in a directory path instead of `.`.

#### Options


- `--out / -o`: The output file is saved as `nb_quality_review.png`  by default. Pass in another name via the `-o myimage.png` flag;
- `--gap / -g`: gap between bands (`float`);
- `--gapcolor / -G`: gap colour (default `lightgrey`);
- `--linewidth / -l`: width of line (`int`);



On a Mac, you may get a warning of the form:

```
2020-07-03 15:34:06.658 Python[46394:645167] ApplePersistenceIgnoreState: Existing state will not be touched. New state will be written to (null)
```

This seems to be a known `matplotlib` issue.


### Use as an API

To generate simple visualisations of the relative size and structure (markdown vs code cells)  of a single Jupyter notebook:

```
from  nb_quality_profile import nb_visualiser as nbv

nbv.nb_vis_parse_nb(PATH_TO_IPYNB_FILE)
```

See `demo.ipynb` for an example.

## Related Blog Posts

The visualisation tool was originally described here: [Fragment -Visualising Jupyter Notebook Structure](https://blog.ouseful.info/2019/12/16/fragment-visualising-jupyter-notebook-structure/)

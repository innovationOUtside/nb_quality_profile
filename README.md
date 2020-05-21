# nb_quality_profile
Simple tools for reviewing the quality of Jupyter notebooks.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/innovationOUtside/nb_quality_profile/master?filepath=demo.ipynb)

At the moment, only a single tool is provided: a visualisation of notebook structure (relative length, structure in terms of markdown vs code cell). Visualisations are of the form:

![](simple_nb_viz.png)

## Installation

Install from this repo:


## Usage

To generate simple visualisations of the relative size and structure (markdown vs code cells)  of a single Jupyter notebook:

```
from  nb_quality_profile import nb_visualiser as nbv

nbv.nb_vis_parse_nb(PATH_TO_IPYNB_FILE)
```

See `demo.ipynb` for an example.

## Related Blog Posts

The visualisation tool was originally described here: [Fragment -Visualising Jupyter Notebook Structure](https://blog.ouseful.info/2019/12/16/fragment-visualising-jupyter-notebook-structure/)

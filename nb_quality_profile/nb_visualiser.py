# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Simple Notebook Visualiser
#
# Simple notebook visualiser for one or more Jupyter notebooks.
#
# Visualises markdown and code cells, with block size determined by code cell line count and estimated screen line count for markdown cells.

# +
import math
import matplotlib.pyplot as plt


def nb_vis(cell_map, img_file='', linewidth = 5, w=20, gap=None, gap_boost=1, gap_colour='lightgrey'):
    """Visualise notebook gross cell structure."""

    def get_gap(cell_map):
        """Automatically set the gap value based on overall length"""
        
        def get_overall_length(cell_map):
            """Get overall line length of a notebook."""
            overall_len = 0
            gap = 0
            for i ,(l,t) in enumerate(cell_map):
                #i is number of cells if that's useful too?
                overall_len = overall_len + l
            return overall_len

        max_overall_len = 0
        
        #If we are generating a plot for multiple notebooks, get the largest overall length
        if isinstance(cell_map,dict):
            for k in cell_map:
                _overall_len = get_overall_length(cell_map[k])
                max_overall_len = _overall_len if _overall_len > max_overall_len else max_overall_len
        else:
            max_overall_len = get_overall_length(cell_map)

        #Set the gap at 0.5% of the overall length
        return math.ceil(max_overall_len * 0.01)
        
        
    def plotter(cell_map, x, y, label='', header_gap = 0.2):
        """Plot visualisation of gross cell structure for a single notebook."""

        #Plot notebook path
        plt.text(y, x, label)
        x = x + header_gap

        for _cell_map in cell_map:

            #Add a coloured bar between cells
            if y > 0:
                if gap_colour:
                    plt.plot([y,y+gap],[x,x], gap_colour, linewidth=linewidth)

                y = y + gap
            
            _y = y + _cell_map[0] + 1 #Make tiny cells slightly bigger
            plt.plot([y,_y],[x,x], _cell_map[1], linewidth=linewidth)

            y = _y
    
    x = 1
    y = 0
    
    gap = gap if gap is not None else get_gap(cell_map) * gap_boost
    fig, ax = plt.subplots(figsize=(w, 1+len(cell_map)))
    plt.text(0, 0, "\nNotebook quality report")
    for k in cell_map:
        plotter(cell_map[k], x, y, k)
        x = x + 1

    ax.axis('off')
    plt.gca().invert_yaxis()
    
    if img_file:
        plt.savefig(img_file)
# -

# Define the colour map for different cell types:

VIS_COLOUR_MAP  = {'markdown':'cornflowerblue','code':'pink'}
LINE_WIDTH = 160

# The following function will find one or more notebooks on a path and generate cell maps for each of them. All the cell maps are then passed for visualisation on the same canvas.

# +
import nbformat
import os
import textwrap
    
def nb_vis_parse_nb(path, img_file='', linewidth = 5, w=20, **kwargs):
                    #gap=None, gap_boost=1, gap):
    """Parse one or more notebooks on a path."""
    
    def _count_screen_lines(txt, width=LINE_WIDTH):
        """Count the number of screen lines that an overflowing text line takes up."""
        ll = txt.split('\n')
        _ll = []
        for l in ll:
            #Model screen flow: split a line if it is more than `width` characters long
            _ll=_ll+textwrap.wrap(l, width)
        n_screen_lines = len(_ll)
        return n_screen_lines
    
    
    def _nb_vis_parse_nb(fn):
        """Parse a notebook and generate the nb_vis cell map for it."""

        cell_map = []

        _fn, fn_ext = os.path.splitext(fn)
        if not fn_ext=='.ipynb' or not os.path.isfile(fn):
            return cell_map

        with open(fn,'r') as f:
            nb = nbformat.reads(f.read(), as_version=4)

        for cell in nb.cells:
            cell_map.append((_count_screen_lines(cell['source']), VIS_COLOUR_MAP[cell['cell_type']]))

        return cell_map

    def _dir_walker(path, exclude = 'default'):
        """Profile all the notebooks in a specific directory and in any child directories."""

        if exclude == 'default':
            exclude_paths = ['.ipynb_checkpoints', '.git', '.ipynb', '__MACOSX']
        else:
            #If we set exclude, we need to pass it as a list
            exclude_paths = exclude
        nb_multidir_cell_map = {}
        for _path, dirs, files in os.walk(path):
            #Start walking...
            #If we're in a directory that is not excluded...
            if not set(exclude_paths).intersection(set(_path.split('/'))):
                #Profile that directory...
                for _f in files:
                    fn = os.path.join(_path, _f)
                    cell_map = _nb_vis_parse_nb(fn)
                    if cell_map:
                        nb_multidir_cell_map = {**nb_multidir_cell_map, fn: cell_map}

        return nb_multidir_cell_map
    
    if os.path.isdir(path):
        cell_map = _dir_walker(path)
    else:
        cell_map = {path: _nb_vis_parse_nb(path)}
        
    nb_vis(cell_map, img_file, linewidth, w, **kwargs)

# + tags=["active-ipynb"]
# Test a single notebook mapper:

# + tags=["active-ipynb"]
# TEST_NOTEBOOK = 'Notebook_profile_test.ipynb'

# + tags=["active-ipynb"]
# nb_vis_parse_nb(TEST_NOTEBOOK)

# + tags=["active-ipynb"]
# Test a plot of multiple notebooks down a path:

# + tags=["active-ipynb"]
# nb_vis_parse_nb('../Documents/GitHub/tm351-undercertainty/notebooks/tm351/Part 02 Notebooks',
#                 linewidth=10, gap_colour='white', gap=1, img_file='test-nbvis.png')

# + tags=["active-ipynb"]
# nb_vis_parse_nb('../Documents/GitHub/tm351-undercertainty/notebooks/tm351/Part 02 Notebooks',
#                 linewidth=10, gap=0, img_file='test-nbvis.png')

# + tags=["active-ipynb"]
# Can we see the saved test file?
#
# ![](test-nbvis.png)

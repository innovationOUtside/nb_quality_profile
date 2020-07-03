import click
from .nb_visualiser import nb_vis_parse_nb

@click.group()
def cli():
	pass

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--out', '-o', default='nb_quality_review.png',  help='Image outfile')
@click.option('--gap', '-g', default=0, type=float, help='Gap')
@click.option('--gapcolor', '-G', default='lightgrey', help='Gap colour')
@click.option('--linewidth', '-l', default=5, type=int, help='Line width')
def chart(path, out, gap, gapcolor, linewidth):
	"""Display notebook profile chart."""
	click.echo('Using file/directory: {}'.format(path))
	#nb_vis_parse_nb('../Documents/GitHub/tm351-undercertainty/notebooks/tm351/Part 02 Notebooks',
    #        linewidth=10, gap=0, img_file='test-nbvis.png')
	nb_vis_parse_nb(path, img_file=out,  linewidth = linewidth, w=20, gap=gap, gap_boost=1, gap_colour=gapcolor)

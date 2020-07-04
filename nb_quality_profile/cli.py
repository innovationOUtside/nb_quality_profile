import click
from .nb_visualiser import nb_vis_parse_nb, nb_imports_parse_nb, nb_text_parse_nb

@click.group()
def cli():
	pass

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--out', '-o', default='nb_quality_review.png',  help='Image outfile')
@click.option('--gap', '-g', default=0, type=float, help='Gap')
@click.option('--gapcolor', '-G', default='lightgrey', help='Gap colour')
@click.option('--linewidth', '-l', default=5, type=int, help='Line width')
@click.option('--text-formats/--no-text-formats', default=True, help="Enable/disable Jupytext support.")
def chart(path, out, gap, gapcolor, linewidth, text_formats):
	"""Display notebook profile chart from provided file or directory path."""
	click.echo('Using file/directory: {}'.format(path))
	#nb_vis_parse_nb('../Documents/GitHub/tm351-undercertainty/notebooks/tm351/Part 02 Notebooks',
    #        linewidth=10, gap=0, img_file='test-nbvis.png')
	nb_vis_parse_nb(path, img_file=out,  linewidth = linewidth,
					w=20, gap=gap, gap_boost=1, gap_colour=gapcolor,
					text_formats=text_formats)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--text-formats/--no-text-formats', default=True, help="Enable/disable Jupytext support.")
def imports(path, text_formats):
	"""Display notebook imports from provided file or directory path."""
	click.echo('Using file/directory: {}'.format(path))
	nb_imports_parse_nb(path, text_formats)

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--text-formats/--no-text-formats', default=True,
			   help="Enable/disable Jupytext support.")
@click.option('--reading-rate', '-r', default=100, type=int, help='Words per minute.')
@click.option('--rounded-minutes', '-R', is_flag=True, help='Round up to minutes.')
def text_analysis(path, text_formats, reading_rate, rounded_minutes):
	"""Report on text / markdown content."""
	click.echo('Using file/directory: {}'.format(path))
	nb_text_parse_nb(path, text_formats, reading_rate, rounded_minutes)
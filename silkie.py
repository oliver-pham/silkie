import click

@click.command()
@click.version_option("0.1.0", '-v', '--version')
@click.help_option('-h', '--help')
def silkie():
    """Static site generator with the smoothness of silk"""
    click.echo("Success!")
    
if __name__ == '__main__':
    silkie()

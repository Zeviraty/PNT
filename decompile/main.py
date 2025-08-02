import click
from header import check_header
import header as h

global VERBOSE
VERBOSE = False

@click.command()
@click.argument("file", type=str)
@click.option("-v","--verbose", default=False, help="Enable more debug printing", is_flag=True)
@click.option("-n","--name",default="rom", help="Name of output files")
def cli(file, verbose, name):
    h.VERBOSE = verbose

    rom = open(file, 'rb').read()
    header = check_header(rom)
    if not header[0]: print("Header is invalid, or isnt placed correctly"); exit(0)
    header = header[1]

    header.to_file(f"{name}.nh")

    if header.trainer:
        vprint("Trainer present")
        trainer = rom[16:528]
        open()

if __name__ == '__main__':
    cli()

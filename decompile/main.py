import click
from header import check_header
import header as h

global VERBOSE
VERBOSE = False

def vprint(txt:str):
    if VERBOSE:
        print(txt)

@click.command()
@click.argument("file", type=str)
@click.option("-v","--verbose", default=False, help="Enable more debug printing", is_flag=True)
@click.option("-n","--name",default="rom", help="Name of output files")
def cli(file, verbose, name):
    h.VERBOSE = verbose
    VERBOSE = verbose

    rom = open(file, 'rb').read()
    header = check_header(rom)
    if not header[0]: print("Header is invalid, or isnt placed correctly"); exit(0)
    header = header[1]

    header.to_file(f"{name}.nh")

    if header.trainer:
        vprint("Trainer present")
        trainer = rom[16:528]
        open(f"{name}.ntr")

        prg = rom[528:header.prg_rom_size]
    else:
        prg = rom[16:header.prg_rom_size+22]

    print(header.prg_rom_size+12)
    print(prg[-4:])

    reset_vector = (prg[-3] << 8) | prg[-4]
    print(f"Reset vector: ${hex(reset_vector)[2:]}")

if __name__ == '__main__':
    cli()

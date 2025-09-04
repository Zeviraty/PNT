'''
Main decompiling file

header.py: Decoding INES and NES2.0 headers
opcodes.json: All 6502 opcodes (taken from https://github.com/Esshahn/pydisass6502/blob/main/lib/opcodes.json)
'''

import click
from header import check_header
import header as h
import os
from utils import set_verbose, vprint

@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("-v","--verbose", default=False, help="Enable more debug printing", is_flag=True)
@click.option("-f","--folder",default=None, help="Folder for output files")
def cli(files, verbose, folder):
    for file in files:
        name = os.path.join(folder,os.path.split(file)[1].split(".")[0])
        decompile(file,verbose,name)

def decompile(file,verbose, name):
    set_verbose(verbose)

    rom = open(file, 'rb').read()
    header = check_header(rom)
    if not header[0]: print("Header is invalid, or isnt placed correctly"); exit(0)
    header = header[1]

    header.to_file(f"{name}.nh")

    if header.trainer:
        vprint("Trainer present")
        trainer = rom[16:528]
        open(f"{name}.ntr",'wb').write(trainer)

        prg = rom[528:header.prg_rom_size+528]
    else:
        prg = rom[16:header.prg_rom_size+16]

    reset_vector = (prg[-3] << 8) | prg[-4]
    vprint(f"Reset vector: ${reset_vector:04x}")

if __name__ == '__main__':
    cli()

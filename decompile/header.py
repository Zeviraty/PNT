from utils import vprint

class INES_header:
    def __init__(self,prg_rom_pages, chr_rom_pages, chr_ram,
                 mapper, four_screen, trainer,
                 battery, mirroring, playchoice_10,
                 vs_unisystem, pad):
        self.prg_rom_pages = prg_rom_pages
        self.prg_rom_size = prg_rom_pages * 16 * 1024
        self.chr_rom_pages = chr_rom_pages
        self.chr_rom_size = chr_rom_pages * 8 * 1024
        self.chr_ram = chr_ram
        self.mapper = mapper
        self.four_screen = four_screen
        self.trainer = trainer
        self.battery = battery
        self.mirroring = mirroring
        self.playchoice_10 = playchoice_10
        self.vs_unisystem = vs_unisystem
        self.pad = pad

    def to_file(self,location: str):
        open(location, 'w').write("")
        file = open(location, 'a')
        file.write("type: INES\n")
        for k,v in vars(self).items():
            file.write(f"{k}: {v}\n")

class NES20_header:
    def __init__(self,prg_rom_pages, chr_rom_pages, chr_ram,
                 mapper, four_screen, trainer,
                 battery, mirroring, playchoice_10,
                 vs_unisystem, sub_mapper, prg_rom_size,
                 chr_rom_size, eeprom, prg_ram_size,
                 chr_ram_size, chr_nvram_size
                 ):
        self.prg_rom_pages = prg_rom_pages
        
        self.chr_rom_pages = chr_rom_pages
        self.chr_ram = chr_ram
        self.mapper = mapper
        self.four_screen = four_screen
        self.trainer = trainer
        self.battery = battery
        self.mirroring = mirroring
        self.playchoice_10 = playchoice_10
        self.vs_unisystem = vs_unisystem
        self.sub_mapper = sub_mapper
        if prg_rom_size != 0:
            self.prg_rom_size = prg_rom_size
        else:
            self.prg_rom_size = prg_rom_pages * 16 * 1024
        if chr_rom_size != 0:
            self.chr_rom_size = chr_rom_size
        else:
            self.chr_rom_size = chr_rom_pages * 8 * 1024
        self.eeprom = eeprom
        self.prg_ram_size = prg_ram_size
        self.chr_ram_size = chr_ram_size
        self.chr_nvram_size = chr_nvram_size

    def to_file(self,location: str):
        open(location, 'w').write("")
        file = open(location, 'a')
        file.write("type: NES 2.0\n")
        for k,v in vars(self).items():
            file.write(f"{k}: {v}\n")

def check_header(rom):
    nes = rom[0:4] == b'NES\x1a'
    if nes:
        vprint("Correct NES identifier")
    else:
        vprint("Incorrect NES identifier")

    prg_rom_pages = int.from_bytes(rom[4:5], 'little')

    if prg_rom_pages == 0:
        vprint("Invalid PRG-ROM in header ROM has 0 PRG-ROM pages.")
        prg_rom_valid = False
    elif prg_rom_pages > 255:
        vprint("Invalid PRG_ROM in header Too many PRG-ROM pages (max 255).")
        prg_rom_valid = False
    else:
        vprint(f"Valid PRG-ROM size: {prg_rom_pages} pages ({prg_rom_pages * 16} KB)")
        prg_rom_valid = True

    expected_size = 16 + (prg_rom_pages * 16 * 1024)
    if len(rom) < expected_size:
        vprint(f"Invalid: File is too small for {prg_rom_pages} PRG-ROM pages.")
    else:
        vprint("File size is correct for defined PRG-ROM size")

    chr_rom_pages = int.from_bytes(rom[5:6], 'little')
    chr_ram = False
    
    if chr_rom_pages == 0:
        vprint("Warning: CHR-ROM size is 0, using CHR-RAM")
        chr_rom_valid = True
        chr_ram = True
    elif chr_rom_pages > 255:
        vprint("Invalid CHR_ROM in header Too many PRG-ROM pages (max 255).")
        chr_rom_valid = False
    else:
        vprint(f"Valid CHR-ROM size: {prg_rom_pages} pages ({prg_rom_pages * 8} KB)")
        chr_rom_valid = True

    expected_size = 16 + (prg_rom_pages * 16 * 1024) + (chr_rom_pages * 8 * 1024)
    if len(rom) < expected_size:
        vprint(f"Invalid: File is too small for {chr_rom_pages} CHR-ROM pages.")
    else:
        vprint("File size is correct for defined CHR-ROM size")

    flags_6 = rom[6]

    mapper_lower = (flags_6 >> 4) & 0b1111
    four_screen = (flags_6 >> 3) & 0b1
    trainer = (flags_6 >> 2) & 0b1
    battery = (flags_6 >> 1) & 0b1
    mirroring = flags_6 & 0b1

    flags_7 = rom[7]

    mapper_upper = (flags_7 >> 4) & 0b1111
    playchoice_10 = (flags_7 >> 1) & 0b1
    vs_unisystem = flags_7 & 0b1

    nes20 = (flags_7 >> 2) & 0b11 == 0b10

    if nes20:
        vprint("File is NES 2.0")
    else:
        vprint("File is INES")

    mapper = (mapper_upper << 4) | mapper_lower

    if nes20:
        flags_8 = rom[8]
        mapper_extra = flags_8 & 0x0F
        mapper |= (mapper_upper << 8)
        sub_mapper = (flags_8 >> 4) & 0x0F

        flags_9 = rom[9]
        prg_rom_size = (flags_9 >> 4) & 0x0F
        chr_rom_size = flags_9 & 0x0F

        flags_10 = rom[10]
        eeprom = (flags_10 >> 4) & 0x0F
        prg_ram_size = flags_10 & 0x0F

        if eeprom == 0:
            vprint("No PRG-NVRAM")
            eeprom = 0
        else:
            eeprom = 64 << eeprom

        if prg_ram_size == 0:
            vprint("No PRG-RAM")
        else:
            prg_ram_size = 64 << prg_ram_size

        flags_11 = rom[11]
        chr_nvram_size = (flags_11 >> 4) & 0x0F
        chr_ram_size = flags_11 & 0x0F

        if chr_nvram_size == 0:
            vprint("No CHR-NVRAM")
            chr_nvram_size = 0
        else:
            chr_nvram_size = 64 << eeprom

        if chr_ram_size == 0:
            vprint("No CHR-RAM")
        else:
            chr_ram_size = 64 << prg_ram_size

        header = NES20_header(prg_rom_pages, chr_rom_pages, chr_ram,
                              mapper, four_screen, trainer,
                              battery, mirroring, playchoice_10,
                              vs_unisystem, sub_mapper, prg_rom_size,
                              chr_rom_size, eeprom, prg_ram_size,
                              chr_ram_size, chr_nvram_size
                 )
    else:
        pad = rom[7:16]
        if pad == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00': pad = ""
        else:
            try: pad = pad.decode()
            except: pad = str(pad)
        header = INES_header(prg_rom_pages, chr_rom_pages, chr_ram,
                 mapper, four_screen, trainer,
                 battery, mirroring, playchoice_10,
                 vs_unisystem, pad)

    return (nes and prg_rom_valid and chr_rom_valid, header)

global VERBOSE
VERBOSE = False

def set_verbose(val):
    global VERBOSE
    VERBOSE = val

def vprint(txt:str):
    if VERBOSE:
        print(txt)

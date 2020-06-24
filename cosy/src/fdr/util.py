

#VERBOSE_SUPER = 4
VERBOSE_HIGH = 3
VERBOSE_MID = 2
VERBOSE_LOW = 1
VERBOSE_NONE = 0

verbosity = VERBOSE_HIGH

def set_verbosity(val):
    if ((val >= VERBOSE_NONE) and (val <= VERBOSE_HIGH)):
        global verbosity
        verbosity = val

def cond_print(msg_verbosity, msg):
    if(msg_verbosity <= verbosity):
        print(msg)


def normalize(s):
    # replace '.' in string s with '_'
    return str.replace(s,'.','_')

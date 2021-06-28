from propargs.constants import *


def try_type_val(val, atype):
    if atype in TYPE_DICT:
        if val is None:
            return TYPE_FOR_NONE[atype]
        else:
            type_cast = TYPE_DICT[atype]
            return type_cast(val)
    else:
        return val


def boolean(val):
    if type(val) is str:
        return val.lower() == 'true' or val.lower() == 'yes'

    if type(val) in (int, float):
        return val == 1

    return bool(val)


TYPE_DICT = {BOOL: boolean, INT: int, FLT: float, CMPLX: complex, STR: str}
TYPE_FOR_NONE = {BOOL: False, INT: 0, FLT: 0.0, CMPLX: 0j, STR: ''}

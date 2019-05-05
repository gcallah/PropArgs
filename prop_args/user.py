
from prop_args.constants import *

def interrogate_user_through_cl(prop_args):
    for prop_nm in prop_args:
        if (hasattr(prop_args.props[prop_nm], QUESTION)
            and prop_args.props[prop_nm].question):
            prop_args.props[prop_nm].val = _ask_until_correct(prop_args, prop_nm)

def _ask_until_correct(prop_args, prop_nm):
    atype = None
    if hasattr(prop_args.props[prop_nm], ATYPE):
        atype = prop_args.props[prop_nm].atype

    while True:
        answer = input(_get_question(prop_args, prop_nm))
        if not answer:
            return prop_args.props[prop_nm].val

        try:
            typed_answer = prop_args._try_type_val(answer, atype)
        except ValueError:
            print("Input of invalid type. Should be {atype}"
                  .format(atype=atype))
            continue

        if not prop_args._answer_within_bounds(prop_nm, typed_answer):
            print("Input must be between {lowval} and {hival} inclusive."
                  .format(lowval=prop_args.props[prop_nm].lowval,
                          hival=prop_args.props[prop_nm].hival))
            continue

        return typed_answer

def _get_question(prop_args, prop_nm):
        return "{question} [{lowval}-{hival}] ({default}) "\
               .format(question=prop_args.props[prop_nm].question,
                       lowval=prop_args.props[prop_nm].lowval,
                       hival=prop_args.props[prop_nm].hival,
                       default=prop_args.props[prop_nm].val)

import os
import platform

from propargs.constants import OS

def set_props_from_env(prop_args):
    env_dict = os.environ
    common_prop_keys = env_dict.keys() & prop_args.props.keys()
    for key in common_prop_keys:
        prop_args[key] = env_dict[key]

    prop_args[OS] = platform.system()

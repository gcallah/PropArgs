import os
import platform

from prop_args.constants import OS

def overwrite_props_from_env(prop_args):
    env_dict = os.environ
    for env_var in env_dict:
        prop_args[env_var] = env_dict[env_var]

    prop_args[OS] = platform.system()

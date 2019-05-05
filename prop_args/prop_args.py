"""
prop_args2.py
Set, read, and write program-wide properties in one location. Includes logging.
"""
import logging
import sys
import json

from prop_args.prop import Prop
from prop_args import data_store, env, property_file, command_line
from prop_args.constants import *


class PropArgs:
    """
    This class holds named properties for program-wide values.
    It enables getting properties from a file, a database,
    or from the user, either via the command line or a prompt.
    """

    @staticmethod
    def create_props(name, ds_file=None, prop_dict=None):
        """
        Create a property object with values in 'props'.
        """
        if prop_dict is None:
            prop_dict = dict()
        return PropArgs(name, ds_file=ds_file, prop_dict=prop_dict)

    def __init__(self, name, logfile=None, ds_file=None, prop_dict=None,
                 loglevel=logging.INFO):
        """
        Loads and sets properties in the following order:
        1. The Database (Not Implemented)
        2. The User's Environment (operating system, dev/prod settings, etc.)
        3. Property File
        4. Command Line
        5. Questions Prompts During Run-Time
        """
        self.name = name
        self.logfile = logfile
        self.ds_file = ds_file
        self.props = prop_dict or dict()

        # 1. The Data Store
        data_store.set_props_from_ds(self)

        # 2. The Environment
        env.overwrite_props_from_env(self)

        # 3. Property File
        property_file.overwrite_props_from_dict(self, prop_dict)

        # 4. process command line args and set them as properties:
        command_line.overwrite_props_from_cl(self)

        if UTYPE in self.props and self.props[UTYPE].val in (TERMINAL, IPYTHON, IPYTHON_NB):

            # 5. Ask the user questions.
            self.overwrite_props_from_user()

        self.logger = Logger(self, name=name, logfile=logfile)

    def overwrite_props_from_user(self):
        for prop_nm in self:
            if (hasattr(self.props[prop_nm], QUESTION)
                and self.props[prop_nm].question):
                self.props[prop_nm].val = self._ask_until_correct(prop_nm)

    @staticmethod
    def _try_type_val(val, atype):
        if atype in type_dict:
            type_cast = type_dict[atype]
            return type_cast(val)
        else:
            return val

    def _ask_until_correct(self, prop_nm):
        atype = None
        if hasattr(self.props[prop_nm], ATYPE):
            atype = self.props[prop_nm].atype

        while True:
            answer = input(self.get_question(prop_nm))
            if not answer:
                return self.props[prop_nm].val

            try:
                typed_answer = self._try_type_val(answer, atype)
            except ValueError:
                print("Input of invalid type. Should be {atype}"
                      .format(atype=atype))
                continue

            if not self._answer_within_bounds(prop_nm, typed_answer):
                print("Input must be between {lowval} and {hival} inclusive."
                      .format(lowval=self.props[prop_nm].lowval,
                              hival=self.props[prop_nm].hival))
                continue

            return typed_answer

    def _answer_within_bounds(self, prop_nm, typed_answer):
        if (self.props[prop_nm].atype is None 
            or self.props[prop_nm].atype in (STR, BOOL)):
            return True

        if (self.props[prop_nm].lowval is not None 
            and self.props[prop_nm].lowval > typed_answer):
            return False

        if (self.props[prop_nm].hival is not None 
            and self.props[prop_nm].hival < typed_answer):
            return False

        return True

    def display(self):
        """
        How to represent the properties on screen.
        """
        ret = "Properties in " + self.name + "\n"
        for prop_nm in self:
            ret += "\t" + prop_nm + ": " + str(self.props[prop_nm].val) + "\n"

        return ret

    def __iter__(self):
        return iter(self.props)

    def __str__(self):
        return self.display()

    def __len__(self):
        return len(self.props)

    def __contains__(self, key):
        return key in self.props

    def __setitem__(self, key, v):
        """
        Set a property value.
        """
        if key in self:
            self.props[key].val = v
        else:
            self.props[key] = Prop(val=v)

    def __getitem__(self, key):
        return self.props[key].val

    def __delitem__(self, key):
        del self.props[key]

    def items(self):
        return self.props.items()

    def get_logfile(self):
        """
        Special get function for logfile name
        """
        return self.props["log_fname"].val

    def write(self, file_nm):
        """
        Write properties to json file.
        Useful for storing interesting parameter sets.
        """
        dict_for_json = {}
        for prop_name in self.props:
            dict_for_json[prop_name] = self.props[prop_name].to_json()
        f = open(file_nm, 'w')
        json.dump(dict_for_json, f, indent=4)
        f.close()

    def to_json(self):
        return { prop_nm: self.props[prop_nm].to_json() for prop_nm in self.props }

    def get(self, key, default=None):
        if key in self.props and self.props[key].val:
            return self.props[key].val
        return default

    def get_question(self, prop_nm):
            return "{question} [{lowval}-{hival}] ({default}) "\
                   .format(question=self.props[prop_nm].question, 
                           lowval=self.props[prop_nm].lowval,
                           hival=self.props[prop_nm].hival,
                           default=self.props[prop_nm].val)


class Logger:
    """
    A class to track how we are logging.
    """

    DEF_FORMAT = '%(asctime)s:%(levelname)s:%(message)s'
    DEF_LEVEL = logging.INFO
    DEF_FILEMODE = 'w'
    # DEF_FILENAME = 'log.txt'

    def __init__(self, props, name, logfile=None,
                 loglevel=logging.INFO):
        if logfile is None:
            logfile = name + ".log"
        fmt = props["log_format"] if "log_format" in props else Logger.DEF_FORMAT
        lvl = props["log_level"] if "log_level" in props else Logger.DEF_LEVEL
        fmd = props["log_fmode"] if "log_fmode" in props else Logger.DEF_FILEMODE
        props["log_fname"] = logfile
# we put the following back in once the model names are fixed
#  fnm = props.get("log_fname", logfile)
        logging.basicConfig(format=fmt,
                            level=lvl,
                            filemode=fmd,
                            filename=logfile)
        logging.info("Logging initialized.")


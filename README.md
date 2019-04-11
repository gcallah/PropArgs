# PropArgs
A module for systematically organizing user preferences acquired from a database, env vars, a parameter file, or user 
choices.

## How it Works

### Overview
PropArgs is initialized by sequentially loading the following five stages of input:

1. Data Store

1. Environment

1. Property File

1. Command Line

1. User

Properties may be defined in only the first two stages, and properties defined in each stage may be replaced
by properties defined in later stages.

Each property has a key and a value and is accessed like a dictionary:

    >>> pa = PropArgs()
    >>> pa["prop_nm"] = 1  # assigns the value 1 to the property "prop_nm"
    >>> pa["prop_name]
    1

In addition to this, each property may have associated metadata - at present: upper bounds, lower bounds, datatype,
and question strings to aid user input.

### Details

#### Data Store
The Data Store is at present limited to only JSON files. In the future databases will be an option. The JSON
formatting is as follows:

    {
        "prop_name_1": {
            "val": "<something>",
            "question": "<something>",
            "atype": "<something>",
            "hival": "<something>",
            "loval": "<something>"
        },
        "prop_name_2": {
            "val": "<something>"
        }
    }

Note that any given property need not have all metadata fields defined in the json. Only the "val" is required.


#### Environment
PropArgs will read and add all the environment variables in program in which PropArgs is initialized.


#### Property File
Currently the only Property File type supported is JSON. The formatting is as follows:

    {
        "prop_name_1": "val_1",
        "prop_name_2": "val_2",
        "prop_name_3": "val_3"
    }


#### Command Line
Properties are defined through the command line through PyArgs formatting.

#### User
The final stage is to ask the user questions for properties that have them. (i.e. the "question" field is nonnull) The
default behavior is to prompt questions in the client's shell:

    >>> pa = PropArgs()
    What is the value of prop_1? ("I'm the default prop value") <enter_value>
    What is the value of prop_2? [0.0-100.0] (20) <enter_value>

However, the client program may want to take over and ask questions in its own way. In this case we may set a flag
that skips the user stage, and instead the client can call `pa.get_questions()` for a JSON of the questions and
metadata.

    >>> pa = PropArgs(skip_user_questions=True)
    >>> pa.get_questions()
    {
        "prop_name_1": {
            "val": "<something>",
            "question": "<something>",
            "atype": "<something>",
            "hival": "<something>",
            "loval": "<something>"
        },
        "prop_name_2": {
            "val": "<something>"
        }
    }

## Credits
Idea - Robert Dodson

Development - Gene Callahan and Nathan Conroy
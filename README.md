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

During the loading process properties may be introduced in any stage except the User stage. A property defined in one
stage may be overwritten in later stages. 

Each property has a key and a value and is accessed like a dictionary:

    >>> pa = PropArgs.create_props()
    >>> pa["prop_nm"] = 1  # assigns the value 1 to the property "prop_nm"
    >>> pa["prop_name]
    1

In addition to this, each property may have associated metadata. These are at present: a question for the
user-input prompt, a datatype, an upper bound, and a lower bound.

### Details

#### Data Store
The Data Store will soon support JSON files. In the future databases will be an option.

The Data Store file is specified on initialization

    PropArgs.create_props(ds_file=file_name)

The JSON formatting is as follows:

    {
        "prop_name_1": {
            "val": "1",
            "question": "What value should this property have?",
            "atype": "int",
            "hival": "10",
            "loval": "0"
        },
        "prop_name_2": {
            "val": "Hello World."
        }
    }

Note that any given property need not have all metadata fields defined in the JSON. Only the "val" is required.


#### Environment
PropArgs will read and add all the environment variables of the program in which PropArgs is initialized.
(i.e. everything in os.environ)


#### Property File
A property file will be specified on initialization by name (and path if in another directory).

    >>> pa = PropArgs.create_props(prop_file=file_name)

Currently the only Property File type supported is JSON. The formatting is the same as the Data Store's 
JSON formatting:

    {
        "prop_name_1": {
            "val": "1",
            "question": "What value should this property have?",
            "atype": "int",
            "hival": "10",
            "loval": "0"
        },
        "prop_name_2": {
            "val": "Hello World."
        }
    }


#### Command Line
Properties will be read from the command line as follows

    $ python program_reading_props.py --props prop_1=val_1,prop_2=val_2,prop_3=val_3  #etc...

#### User
The final stage is to ask the user to define properties for properties that have question metadata.
The default behavior is to prompt questions in the client's shell:

    >>> pa = PropArgs.create_props()
    What is the value of prop_1? ("I'm the default prop value") <enter_value>
    What is the value of prop_2? [0.0-100.0] (20) <enter_value>

However, the client program may want to take over and ask questions in its own way. In this case we will provide a flag
that skips the user stage, and instead the client will call `pa.get_questions()` for a JSON of the properties with
questions.

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
            "val": "<something>",
            "questoin": <something>
        }
    }

## Credits
Idea - Robert Dodson

Development - Gene Callahan and Nathan Conroy

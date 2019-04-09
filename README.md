# PropArgs
A module for systematically organizing user preferences acquired from a database, env vars, a parameter file, or user 
choices.

## How it Works

### Overview
Your PropArgs is initialized by sequentially loading the following five stages of input:

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
The Data Stores are at present limited to only JSON files. In the future databases will be an option. The JSON
formatting is as follows:

    {
        prop_name:
            {
                val: <something>,
                question: <something>,
                atype: <something>,
                hival: <something>,
                loval: <something>
            }
        prop_name:
            {
                val: <something>,
            }
    }

Note that any given property need not have all metadata defined.


#### Environment
PropArgs will read and add all the environment variables in program in which PropArgs is initialized.


#### Property File
Currently the only Property File type supported is JSON. The formatting is as follows:

    {
        prop_name_1: val_1,
        prop_name_2: val_2,
        prop_name_3: val_3
    }


#### Command Line
Properties are defined through the command line through PyArgs formatting.

#### User
The final stage is to ask the user questions for properties that have them.

At this point, the client program may want to take over. If the client program sets a flag,
we will return an iterator with which the client may iterate over the questions and ask them
in the way it wants.

## Credits
Idea - Robert Dodson

Development - Gene Callahan and Nathan Conroy
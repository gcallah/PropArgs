"""
Methods the Data Store import process
"""
import json

def set_props_from_ds(prop_args):
    if prop_args.ds_file:
        ds_dict = _open_file_as_json(prop_args.ds_file)
        prop_args.overwrite_props_from_dict(ds_dict)


def _open_file_as_json(ds_file):
    with open(ds_file, 'r') as f:
        ds_dict = json.load(f)
    return ds_dict
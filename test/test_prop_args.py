#!/usr/bin/env python3
"""
This is a simple test script. It can be cloned to
create new run scripts, and should be run to test
the system after library changes.
"""
import pytest
import json
from unittest.mock import patch

from prop_args import prop_args as pa

DUMMY_PROP_NM = "dummy_prop"
ANSWERS_FOR_INPUT_PROMPTS = [1]

@pytest.fixture
def prop_args():
    """
    A bare-bones prop_args object. To use - make `prop_args` a test argument.
    """
    return pa.PropArgs.create_props("test_pa", prop_dict=None)


@pytest.mark.parametrize('lowval, test_val, hival, expected', [
        (None,  7, None, True),
        (None, -5,   10, True),
        (0,    99, None, True),
        (0,     7,   10, True),
        (0,    77,   10, False),
        (0,    -5,   10, False)
        ])
def test_int_bounds(lowval, test_val, hival, expected, prop_args):
    prop_args.props[DUMMY_PROP_NM] = pa.Prop(lowval=lowval,
                                             hival=hival,
                                             atype=pa.INT)

    assert prop_args._answer_within_bounds(prop_nm=DUMMY_PROP_NM,
                                           typed_answer=test_val) \
           == expected


def test_props_overwriting_through_prop_file(prop_args):
    prop_json = "{{ \"{prop_name}\": {{\"val\": 7}} }}".format(prop_name=DUMMY_PROP_NM)
    prop_dict = json.loads(prop_json)
    prop_args[DUMMY_PROP_NM] = 100
    prop_args.overwrite_props_from_dict(prop_dict)

    assert prop_args[DUMMY_PROP_NM] == 7


def test_user_input(prop_args):
    prop_args.props[DUMMY_PROP_NM] = pa.Prop(atype=pa.INT,
                                             question="Enter Integer: ",
                                             val=0)

    with patch('builtins.input', side_effect=ANSWERS_FOR_INPUT_PROMPTS):
        prop_args.overwrite_props_from_user()

    assert prop_args[DUMMY_PROP_NM] == ANSWERS_FOR_INPUT_PROMPTS[0]

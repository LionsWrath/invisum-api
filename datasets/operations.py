from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import APIException
import pandas as pd

def args_dict(kwargs, possible):
    args = {}
    for k, v in kwargs.iteritems():
        if k in possible:
            args[k] = v
    return args

# dummy function
def empty(dataframe, *args, **kwargs):
    print dataframe
    print kwargs

    raise APIException(_("This operation does not exist."))

    return dataframe

# Fillna - column or line
# emptystr - column or line - subs
def clean(dataframe, *args, **kwargs):
    print dataframe
    print kwargs

    return dataframe

# Count the values on a column or line
# Maybe generate a ney set
# Create a series
def count(dataframe, *args, **kwargs):
    print dataframe
    print kwargs

    return dataframe

# left, right, step
# Use exceptions after
def slice(dataframe, *args, **kwargs):
    if 'left' in kwargs:
        try:
            left = int(kwargs['left'])
        except ValueError:
            raise ParseError(_("Wrong value for left."))
    else:
        left = 0

    if 'right' in kwargs:
        try:
            right = int(kwargs['right'])
        except ValueError:
            raise ParseError(_("Wrong value for right."))
    else:
        right = len(dataframe.index)

    if 'step' in kwargs:
        try:
            step = int(kwargs['step'])
        except ValueError:
            raise ParseError(_("Wrong value for step."))
    else:
        step = 1

    return dataframe[left:right:step]

# Multiple Dataset Operations ------------------------------------------------
# Move this to another file

def merge(left_dataframe, right_dataframe, *args, **kwargs):
    possible_arguments = {'how', 'on', 'left_on', 'right_on', 'left_index', 'right_index', 'sort', 'suffixes', 'copy', 'indicator'}

    p_args = args_dict(kwargs, possible_arguments)
    
    return left_dataframe.merge(right_dataframe, **p_args)

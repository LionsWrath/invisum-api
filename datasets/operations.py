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
    print dataframe.dtypes

    raise APIException(_("This operation does not exist."))

def dropna(dataframe, *args, **kwargs):
    possible_arguments = {'how'}

    p_args = args_dict(kwargs, possible_arguments)
    
    return dataframe.dropna(**p_args)

def fillna(dataframe, *args, **kwargs):
    possible_arguments = {'value'}

    p_args = args_dict(kwargs, possible_arguments)
    
    return dataframe.fillna(**p_args)

def drop(dataframe, *args, **kwargs):
    possible_arguments = {'labels'}

    p_args = args_dict(kwargs, possible_arguments)
    
    return dataframe.drop(**p_args)

def filter(dataframe, *args, **kwargs):
    possible_arguments = {'items', 'like', 'regex', 'axis'}

    p_args = args_dict(kwargs, possible_arguments)
    
    return dataframe.filter(**p_args)

def sort(dataframe, *args, **kwargs):
    possible_arguments = {'columns', 'ascending', 'axis', 'na_position'}

    p_args = args_dict(kwargs, possible_arguments)
    
    return dataframe.sort(**p_args)



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

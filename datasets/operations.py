from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ParseError
import pandas as pd

# dummy function
def empty(dataframe, *args, **kwargs):
    print dataframe
    print kwargs

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

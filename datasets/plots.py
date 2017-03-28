from bokeh.charts import Histogram, Bar
from bokeh.charts import save, output_file
from django.conf import settings
from os import path
import uuid

htmlpath = path.join(settings.MEDIA_ROOT, 'html')
tools = "pan,wheel_zoom,box_zoom,save,reset"

def generate_path():
    filename = '.'.join([str(uuid.uuid4()), "html"])
    filepath = path.join(htmlpath, filename)
    return filepath

def args_dict(kwargs, possible):
    args = {}
    for k, v in kwargs.iteritems():
        if k in possible:
            args[k] = v
    return args

def create_histogram(dataframe, *args, **kwargs):
    filepath = generate_path()
    possible_arguments = {}

    p_args = args_dict(kwargs, possible_arguments)

    chart = Histogram(dataframe, toolbar_location="above", tools=tools, responsive=True, **p_args)
    chart.toolbar.logo = None

    output_file(filepath)
    save(chart, title="Invisum Plot")

    return path.basename(filepath)

def create_bar(dataframe, *args, **kwargs):
    filepath = generate_path()
    possible_arguments = {'values', 'label', 'plot_width', 'plot_height', 'legend'}

    p_args = args_dict(kwargs, possible_arguments)

    chart = Bar(dataframe, toolbar_location="above", tools=tools, responsive=True, **p_args)
    chart.toolbar.logo = None

    output_file(filepath)
    save(chart, title="Invisum Plot")

    return path.basename(filepath)

# -*- coding: utf-8 -*-
"""
    app.forms
    ~~~~~~~~~

    Basic forms for use throughout application
"""
from wtforms import SelectMultipleField, widgets


class MultiCheckboxField(SelectMultipleField):
    """Base for creating checkbox fields with multiple answers applicable"""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# -*- coding: utf-8 -*-
"""
    fact-store
    ~~~~~~~~~~

    Helper functions to write xAPI data to the fact store.
"""

from flask import current_app


def write_to_fact_store(line):
    with open(current_app.config['FACT_STORE'], 'w+') as f:
        f.writelines([line])

# -*- coding: utf-8 -*-
# Dummy Search Engine

# Wiley Intelligent Solutions, 2018
# John Wiley & Sons, Inc.

# coding: utf-8

import time


def run_query(duration, string):
    """
    All this does is sleep for duration. Add your own database queries, SKLearn magic,
    kitchen prose and gutter rhymes here.
    """
    time.sleep(duration)
    return '4000 holes in {}'.format(string)
